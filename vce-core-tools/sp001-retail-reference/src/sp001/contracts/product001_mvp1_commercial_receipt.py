"""Gate attestation of a committed commercial decision and its audit row."""

from dataclasses import asdict, dataclass
import json
import re

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from sp001.contracts.product001_mvp1_commitment_certificate import (
    CommitmentCertificateV1,
    CommitmentContextV1,
    commitment_certificate_digest,
)


@dataclass(frozen=True, slots=True)
class CommercialReceiptStatementV1:
    gate_id: str
    context: CommitmentContextV1
    certificate_digest: str
    audit_sequence: int
    audit_digest: str

    def __post_init__(self):
        if type(self.gate_id) is not str or not self.gate_id:
            raise ValueError("Gate identity required")
        if type(self.context) is not CommitmentContextV1:
            raise TypeError("commitment context required")
        for digest in (self.certificate_digest, self.audit_digest):
            if type(digest) is not str or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
                raise ValueError("invalid receipt digest")
        if type(self.audit_sequence) is not int or self.audit_sequence <= 0:
            raise ValueError("invalid audit sequence")


@dataclass(frozen=True, slots=True)
class CommercialReceiptV1:
    statement: CommercialReceiptStatementV1
    signature: bytes

    def __post_init__(self):
        if type(self.statement) is not CommercialReceiptStatementV1:
            raise TypeError("commercial receipt statement required")
        if type(self.signature) is not bytes or len(self.signature) != 64:
            raise ValueError("invalid receipt signature")


def commercial_receipt_signing_payload(statement: CommercialReceiptStatementV1) -> bytes:
    return json.dumps(
        {"domain": "SP001/PRODUCT001/MVP1/COMMERCIAL_RECEIPT/V1", **asdict(statement)},
        sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False,
    ).encode("ascii")


def verify_commercial_receipt(
    receipt: CommercialReceiptV1,
    *,
    certificate: CommitmentCertificateV1,
    trusted_gate_id: str,
    trusted_gate_key: Ed25519PublicKey,
) -> None:
    """Verify the Gate attestation against the exact supplied certificate."""
    if type(receipt) is not CommercialReceiptV1:
        raise TypeError("commercial receipt required")
    if type(certificate) is not CommitmentCertificateV1:
        raise TypeError("commitment certificate required")
    if not isinstance(trusted_gate_key, Ed25519PublicKey):
        raise TypeError("trusted Gate key required")
    statement = receipt.statement
    if (
        statement.gate_id != trusted_gate_id
        or statement.context != certificate.context
        or statement.certificate_digest != commitment_certificate_digest(certificate)
    ):
        raise PermissionError("commercial receipt context mismatch")
    try:
        trusted_gate_key.verify(receipt.signature, commercial_receipt_signing_payload(statement))
    except InvalidSignature as error:
        raise PermissionError("invalid commercial receipt signature") from error
