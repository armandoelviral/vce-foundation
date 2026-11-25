"""Experimental signed execution Gate for PRODUCT-001.

Functional integration only. No OS isolation or production key custody.
"""

from collections.abc import Callable
from dataclasses import asdict, dataclass
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PublicKey,
)

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.product001_commercial_approval_decision import (
    Product001CommercialApprovalDecision,
)

from sp001.contracts.product001_mvp1_commitment_certificate import (
    CommitmentCertificateV1,
    CommitmentContextV1,
    verify_commitment_certificate,
)


DOMAIN = "SP001:PRODUCT001:MVP1:APPROVE_PLANOGRAM_VERSION:V1"


def authorization_payload(decision):
    if not isinstance(decision, Product001CommercialApprovalDecision):
        raise TypeError("invalid decision")
    return json.dumps(
        {
            "domain": DOMAIN,
            "decision": asdict(decision),
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


@dataclass(frozen=True, slots=True)
class MVP1Authorization:
    signature: bytes


@dataclass(frozen=True, slots=True)
class MVP1CommitmentAdmission:
    """Gate-owned trust configuration and expected-context lookup."""

    public_key: Ed25519PublicKey
    resolve_context: Callable[[str, str], CommitmentContextV1 | None]
    clock: Callable[[], int]

    def __post_init__(self):
        if not isinstance(self.public_key, Ed25519PublicKey):
            raise TypeError("trusted commitment key required")
        if not callable(self.resolve_context) or not callable(self.clock):
            raise TypeError("trusted context resolver and clock required")

    def verify(self, *, authorization, decision):
        if type(authorization) is not CommitmentCertificateV1:
            raise PermissionError("durable commitment certificate required")
        organization_id = decision.document_scope.organization_id
        operation_id = decision.decision_id
        expected = self.resolve_context(organization_id, operation_id)
        if (
            type(expected) is not CommitmentContextV1
            or expected.organization_id != organization_id
            or expected.operation_id != operation_id
        ):
            raise PermissionError("trusted commitment context unavailable")
        verify_commitment_certificate(
            authorization,
            trusted_key=self.public_key,
            expected_context=expected,
            decision_bytes=authorization_payload(decision),
            now=self.clock(),
        )


def configure_mvp1_admission(*, authority_public_key, commitment_admission):
    if commitment_admission is not None:
        if type(commitment_admission) is not MVP1CommitmentAdmission:
            raise TypeError("invalid commitment admission configuration")
        if authority_public_key is not None:
            raise TypeError("configure exactly one admission mode")
        return commitment_admission.verify
    if not isinstance(authority_public_key, Ed25519PublicKey):
        raise TypeError("trusted authority public key required")

    def verify_legacy(*, authorization, decision):
        if not isinstance(authorization, MVP1Authorization):
            raise PermissionError("external authorization required")
        signature = authorization.signature
        if type(signature) is not bytes or len(signature) != 64:
            raise PermissionError("invalid authorization signature")
        try:
            authority_public_key.verify(signature, authorization_payload(decision))
        except InvalidSignature as exc:
            raise PermissionError("external authorization rejected") from exc

    return verify_legacy


class Product001MVP1ExecutionGate:
    def __init__(
        self, *, writer, authority_public_key=None, commitment_admission=None,
    ):
        if not callable(getattr(writer, "save_decision", None)):
            raise TypeError("writer must implement save_decision")
        self._verify_authorization = configure_mvp1_admission(
            authority_public_key=authority_public_key,
            commitment_admission=commitment_admission,
        )
        self._writer = writer

    def record(
        self,
        *,
        authorization,
        decision: Product001CommercialApprovalDecision,
        authenticated_principal: AuthenticatedPrincipal,
    ) -> bool:
        if not isinstance(
            authenticated_principal, AuthenticatedPrincipal
        ):
            raise TypeError("invalid authenticated principal")

        if not isinstance(
            decision, Product001CommercialApprovalDecision
        ):
            raise TypeError("invalid decision")

        if decision.principal != authenticated_principal:
            raise PermissionError("principal mismatch")

        self._verify_authorization(authorization=authorization, decision=decision)
        return self._writer.save_decision(
            decision=decision,
            authenticated_principal=authenticated_principal,
        )
