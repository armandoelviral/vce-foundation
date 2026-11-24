"""D5.4B.1: pure, non-executive eligibility assessment.

A positive result is a snapshot-relative observation, never admission,
reservation, consumption, or permission to materialize an effect.
"""
from dataclasses import dataclass
from enum import Enum
import hashlib
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from sp001.contracts.product001_documentary_commitment import Product001DocumentaryCommitmentKey
from sp001.contracts.product001_mvp1_contextual_authorization import (
    ContextualAuthorizationV1, authorization_signing_payload,
    verify_contextual_authorization_signature,
)

SNAPSHOT_DOMAIN = "SP001/PRODUCT001/MVP1/AUTHORITY_SNAPSHOT/V1"


class EligibilityStatus(str, Enum):
    ELIGIBLE = "ELIGIBLE"
    REJECTED = "REJECTED"
    INDETERMINATE = "INDETERMINATE"


@dataclass(frozen=True, slots=True)
class AuthorizationEligibilityResultV1:
    status: EligibilityStatus
    reason: str


@dataclass(frozen=True, slots=True)
class AuthoritativeAuthorizationSnapshotV1:
    """Signed observation, not a consumption lock or commitment certificate."""
    issuer_id: str
    operation_id: str
    authorization_digest: str
    revision: int
    authority_sequence: int
    revoked: bool
    consumed: bool
    observed_at: int
    signature: bytes

    def __post_init__(self) -> None:
        if not self.issuer_id or not self.operation_id or any(
            type(v) is not str for v in (self.issuer_id, self.operation_id)
        ):
            raise ValueError("invalid snapshot identity")
        if (type(self.authorization_digest) is not str or
            len(self.authorization_digest) != 64 or
            any(c not in "0123456789abcdef" for c in self.authorization_digest)):
            raise ValueError("invalid authorization digest")
        for field in ("revision", "authority_sequence", "observed_at"):
            value = getattr(self, field)
            if type(value) is not int or value < 0:
                raise ValueError(f"invalid {field}")
        if type(self.revoked) is not bool or type(self.consumed) is not bool:
            raise ValueError("invalid snapshot flags")
        if type(self.signature) is not bytes or len(self.signature) != 64:
            raise ValueError("invalid snapshot signature")


def snapshot_signing_payload(snapshot: AuthoritativeAuthorizationSnapshotV1) -> bytes:
    if type(snapshot) is not AuthoritativeAuthorizationSnapshotV1:
        raise TypeError("snapshot required")
    body = {
        "domain": SNAPSHOT_DOMAIN,
        "issuer_id": snapshot.issuer_id,
        "operation_id": snapshot.operation_id,
        "authorization_digest": snapshot.authorization_digest,
        "revision": snapshot.revision,
        "authority_sequence": snapshot.authority_sequence,
        "revoked": snapshot.revoked,
        "consumed": snapshot.consumed,
        "observed_at": snapshot.observed_at,
    }
    return json.dumps(body, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def authorization_digest(cert: ContextualAuthorizationV1) -> str:
    """Bind the snapshot to the signed certificate including its signature."""
    return hashlib.sha256(authorization_signing_payload(cert) + cert.signature).hexdigest()


def evaluate_authorization_eligibility(
    cert: ContextualAuthorizationV1,
    snapshot: AuthoritativeAuthorizationSnapshotV1 | None,
    *,
    trusted_issuer_id: str,
    trusted_authorization_key: Ed25519PublicKey,
    trusted_snapshot_key: Ed25519PublicKey,
    expected_operation_id: str,
    expected_decision_digest: str,
    expected_documentary_key: Product001DocumentaryCommitmentKey,
    now: int,
    max_snapshot_age: int,
) -> AuthorizationEligibilityResultV1:
    """Verify two signatures and evaluate a bounded observation, without side effects.

    Trusted keys must be provisioned independently of the commercial host.
    No atomic consumption, global latest-revision proof, or prior sealed
    commitment exception is established by this function.
    """
    if type(now) is not int or now < 0 or type(max_snapshot_age) is not int or max_snapshot_age < 0:
        raise ValueError("invalid evaluation time policy")
    if not isinstance(trusted_snapshot_key, Ed25519PublicKey):
        raise TypeError("trusted snapshot key required")
    try:
        verify_contextual_authorization_signature(
            cert, trusted_issuer_id=trusted_issuer_id,
            trusted_public_key=trusted_authorization_key,
            expected_operation_id=expected_operation_id,
            expected_decision_digest=expected_decision_digest,
            expected_documentary_key=expected_documentary_key,
        )
    except (PermissionError, TypeError, ValueError):
        return AuthorizationEligibilityResultV1(EligibilityStatus.REJECTED, "AUTHORIZATION_INVALID")
    if snapshot is None:
        return AuthorizationEligibilityResultV1(EligibilityStatus.INDETERMINATE, "SNAPSHOT_UNAVAILABLE")
    if type(snapshot) is not AuthoritativeAuthorizationSnapshotV1:
        return AuthorizationEligibilityResultV1(EligibilityStatus.INDETERMINATE, "SNAPSHOT_INVALID")
    try:
        trusted_snapshot_key.verify(snapshot.signature, snapshot_signing_payload(snapshot))
    except (InvalidSignature, ValueError):
        return AuthorizationEligibilityResultV1(EligibilityStatus.INDETERMINATE, "SNAPSHOT_SIGNATURE_INVALID")
    if (snapshot.issuer_id != cert.issuer_id or
        snapshot.operation_id != cert.operation_id or
        snapshot.authorization_digest != authorization_digest(cert)):
        return AuthorizationEligibilityResultV1(EligibilityStatus.INDETERMINATE, "SNAPSHOT_CONTEXT_MISMATCH")
    if snapshot.observed_at > now or now - snapshot.observed_at > max_snapshot_age:
        return AuthorizationEligibilityResultV1(EligibilityStatus.INDETERMINATE, "SNAPSHOT_NOT_FRESH")
    if now >= cert.materialize_deadline:
        return AuthorizationEligibilityResultV1(EligibilityStatus.REJECTED, "DEADLINE_EXPIRED")
    if snapshot.authority_sequence < cert.authority_sequence:
        return AuthorizationEligibilityResultV1(EligibilityStatus.INDETERMINATE, "SEQUENCE_BEHIND")
    if snapshot.authority_sequence > cert.authority_sequence:
        return AuthorizationEligibilityResultV1(EligibilityStatus.REJECTED, "SEQUENCE_SUPERSEDED")
    if snapshot.revoked:
        return AuthorizationEligibilityResultV1(EligibilityStatus.REJECTED, "REVOKED_NO_SEALED_COMMITMENT_PROOF")
    if snapshot.consumed:
        return AuthorizationEligibilityResultV1(EligibilityStatus.REJECTED, "ALREADY_CONSUMED")
    return AuthorizationEligibilityResultV1(EligibilityStatus.ELIGIBLE, "SNAPSHOT_RELATIVE_ONLY")
