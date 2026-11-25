"""Independent, read-only verification of a historical commercial record."""

from contextlib import closing
from dataclasses import asdict, dataclass
from enum import StrEnum
import json
from pathlib import Path
import sqlite3

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from sp001.contracts.product001_mvp1_commitment_certificate import (
    CommitmentCertificateV1,
    commitment_certificate_digest,
    verify_commitment_signature,
)
from sp001.contracts.product001_mvp1_contextual_authorization import (
    decision_digest_from_canonical_bytes,
)
from sp001.infrastructure.product001_mvp1_http_codec import decode_product001_mvp1_decision
from sp001.services.product001_mvp1_execution_gate import authorization_payload


class CommercialEvidenceStatus(StrEnum):
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    INDETERMINATE = "INDETERMINATE"


@dataclass(frozen=True, slots=True)
class VerifiedCommercialAudit:
    sequence: int
    canonical_record: str


def _canonical_object(serialized: str) -> dict:
    value = json.loads(serialized)
    if not isinstance(value, dict) or _canonical(value) != serialized:
        raise ValueError("invalid canonical commercial record")
    return value


def _canonical(value: dict) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def read_verified_commercial_audit(
    *,
    database_path: str | Path,
    certificate: CommitmentCertificateV1,
    trusted_key: Ed25519PublicKey,
    trusted_issuer_id: str,
) -> VerifiedCommercialAudit | CommercialEvidenceStatus:
    """Verify correspondence in a supplied database snapshot.

    The caller provisions issuer and key independently. The result carries
    no claim about the authenticity of the SQLite source or time of commit.
    """
    if type(trusted_issuer_id) is not str or not trusted_issuer_id:
        raise ValueError("trusted issuer identity required")
    try:
        verify_commitment_signature(certificate, trusted_key=trusted_key)
    except PermissionError:
        return CommercialEvidenceStatus.REJECTED

    context = certificate.context
    if context.issuer_id != trusted_issuer_id:
        return CommercialEvidenceStatus.REJECTED

    target = Path(database_path).resolve().as_uri() + "?mode=ro"
    try:
        with closing(sqlite3.connect(target, uri=True)) as db:
            row = db.execute(
                """
                SELECT decision.grant_id, decision.definition, audit.sequence, audit.record
                FROM product001_commercial_decisions AS decision
                LEFT JOIN product001_commercial_decision_audit AS audit USING (decision_id)
                WHERE decision.decision_id = ?
                """,
                (context.operation_id,),
            ).fetchone()
    except sqlite3.Error:
        return CommercialEvidenceStatus.INDETERMINATE
    if row is None:
        return CommercialEvidenceStatus.INDETERMINATE

    grant_id, definition, sequence, record = row
    try:
        decision = decode_product001_mvp1_decision(_canonical_object(definition))
        digest = decision_digest_from_canonical_bytes(authorization_payload(decision))
        if (
            decision.decision_id != context.operation_id
            or decision.document_scope.organization_id != context.organization_id
            or decision.authorization_grant_id != grant_id
            or digest != context.decision_digest
        ):
            return CommercialEvidenceStatus.REJECTED
        if record is None:
            return CommercialEvidenceStatus.INDETERMINATE

        if type(sequence) is not int or sequence <= 0:
            return CommercialEvidenceStatus.REJECTED
        audit = _canonical_object(record)
        expected = {
            "action": "RECORD_DECISION",
            "decision_id": context.operation_id,
            "grant_id": grant_id,
            "definition": definition,
        }
        if "commitment" not in audit:
            if audit == expected:
                return CommercialEvidenceStatus.INDETERMINATE
            return CommercialEvidenceStatus.REJECTED
        expected["commitment"] = {
            "version": 1,
            "certificate_digest": commitment_certificate_digest(certificate),
            "context": asdict(context),
        }
        if record != _canonical(expected):
            return CommercialEvidenceStatus.REJECTED
    except (TypeError, ValueError, RecursionError):
        return CommercialEvidenceStatus.REJECTED
    return VerifiedCommercialAudit(sequence, record)


def verify_commercial_evidence(
    *,
    database_path: str | Path,
    certificate: CommitmentCertificateV1,
    trusted_key: Ed25519PublicKey,
    trusted_issuer_id: str,
) -> CommercialEvidenceStatus:
    result = read_verified_commercial_audit(
        database_path=database_path,
        certificate=certificate,
        trusted_key=trusted_key,
        trusted_issuer_id=trusted_issuer_id,
    )
    if isinstance(result, VerifiedCommercialAudit):
        return CommercialEvidenceStatus.VERIFIED
    return result
