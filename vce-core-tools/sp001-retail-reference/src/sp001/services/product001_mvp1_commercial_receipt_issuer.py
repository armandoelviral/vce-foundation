"""Issue a deterministic receipt from the Gate's committed SQLite evidence."""

from hashlib import sha256
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from sp001.contracts.product001_mvp1_commercial_receipt import (
    CommercialReceiptStatementV1,
    CommercialReceiptV1,
    commercial_receipt_signing_payload,
)
from sp001.contracts.product001_mvp1_commitment_certificate import (
    CommitmentCertificateV1,
    commitment_certificate_digest,
)
from sp001.infrastructure.product001_mvp1_commercial_evidence import (
    CommercialEvidenceStatus,
    read_verified_commercial_audit,
)


class Mvp1CommercialReceiptIssuer:
    """Internal Gate service. Configure the database and keys at composition time."""

    def __init__(
        self, *, database_path: str | Path, gate_id: str, signing_key: Ed25519PrivateKey,
        trusted_issuer_id: str, trusted_authority_key: Ed25519PublicKey,
    ):
        if not isinstance(signing_key, Ed25519PrivateKey):
            raise TypeError("Gate signing key required")
        if not isinstance(trusted_authority_key, Ed25519PublicKey):
            raise TypeError("trusted authority key required")
        if signing_key.public_key().public_bytes_raw() == trusted_authority_key.public_bytes_raw():
            raise ValueError("Gate signing key must be distinct from authority key")
        self._database_path = Path(database_path).resolve()
        self._gate_id = gate_id
        self._signing_key = signing_key
        self._issuer_id = trusted_issuer_id
        self._authority_key = trusted_authority_key

    def recover(
        self, certificate: CommitmentCertificateV1,
    ) -> CommercialReceiptV1 | CommercialEvidenceStatus:
        audit = read_verified_commercial_audit(
            database_path=self._database_path,
            certificate=certificate,
            trusted_key=self._authority_key,
            trusted_issuer_id=self._issuer_id,
        )
        if isinstance(audit, CommercialEvidenceStatus):
            return audit
        statement = CommercialReceiptStatementV1(
            gate_id=self._gate_id,
            context=certificate.context,
            certificate_digest=commitment_certificate_digest(certificate),
            audit_sequence=audit.sequence,
            audit_digest=sha256(audit.canonical_record.encode("ascii")).hexdigest(),
        )
        return CommercialReceiptV1(
            statement, self._signing_key.sign(commercial_receipt_signing_payload(statement)),
        )
