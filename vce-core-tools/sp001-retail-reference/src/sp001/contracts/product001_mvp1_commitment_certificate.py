"""Portable proof of a durable MVP1 commitment issued by the authority."""

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from sp001.contracts.product001_mvp1_contextual_authorization import (
    decision_digest_from_canonical_bytes,
)

_DOMAIN = "SP001/PRODUCT001/MVP1/DURABLE_COMMITMENT/V1"


@dataclass(frozen=True, slots=True)
class CommitmentContextV1:
    issuer_id: str
    organization_id: str
    operation_id: str
    authorization_digest: str
    decision_digest: str
    materialize_deadline: int

    def __post_init__(self):
        for value in (self.issuer_id, self.organization_id, self.operation_id):
            if type(value) is not str or not value:
                raise ValueError("invalid commitment identity")
        for value in (self.authorization_digest, self.decision_digest):
            if type(value) is not str or re.fullmatch(r"[0-9a-f]{64}", value) is None:
                raise ValueError("invalid commitment digest")
        if type(self.materialize_deadline) is not int or self.materialize_deadline < 0:
            raise ValueError("invalid commitment deadline")


@dataclass(frozen=True, slots=True)
class CommitmentCertificateV1:
    context: CommitmentContextV1
    signature: bytes

    def __post_init__(self):
        if type(self.context) is not CommitmentContextV1:
            raise TypeError("commitment context required")
        if type(self.signature) is not bytes or len(self.signature) != 64:
            raise ValueError("invalid commitment signature")


def commitment_signing_payload(context: CommitmentContextV1) -> bytes:
    return json.dumps(
        {"domain": _DOMAIN, **asdict(context)},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def commitment_certificate_digest(certificate: CommitmentCertificateV1) -> str:
    """Identify the exact signed certificate independently of its wire encoding."""
    return sha256(
        b"SP001/PRODUCT001/MVP1/COMMITMENT_DIGEST/V1\0"
        + commitment_signing_payload(certificate.context)
        + certificate.signature
    ).hexdigest()


def verify_commitment_certificate(
    certificate: CommitmentCertificateV1,
    *,
    trusted_key: Ed25519PublicKey,
    expected_context: CommitmentContextV1,
    decision_bytes: bytes,
    now: int,
) -> None:
    """Verify an exact commitment using trusted context and a trusted clock."""
    if type(certificate) is not CommitmentCertificateV1:
        raise TypeError("commitment certificate required")
    if type(expected_context) is not CommitmentContextV1:
        raise TypeError("expected commitment context required")
    if not isinstance(trusted_key, Ed25519PublicKey):
        raise TypeError("trusted commitment key required")
    if type(now) is not int or now < 0:
        raise ValueError("invalid verification time")
    if (
        certificate.context != expected_context
        or decision_digest_from_canonical_bytes(decision_bytes)
        != expected_context.decision_digest
    ):
        raise PermissionError("commitment context mismatch")
    try:
        trusted_key.verify(
            certificate.signature, commitment_signing_payload(certificate.context),
        )
    except InvalidSignature as error:
        raise PermissionError("invalid commitment signature") from error
    if now >= certificate.context.materialize_deadline:
        raise PermissionError("commitment deadline expired")
