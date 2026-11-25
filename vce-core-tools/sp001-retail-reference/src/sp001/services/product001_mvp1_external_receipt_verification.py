"""Verify exported commercial evidence using independently configured public keys."""

from dataclasses import asdict
from hashlib import sha256
import json

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from sp001.contracts.product001_mvp1_commercial_receipt import (
    CommercialReceiptV1,
    verify_commercial_receipt,
)
from sp001.contracts.product001_mvp1_commitment_certificate import (
    CommitmentCertificateV1,
    verify_commitment_signature,
)
from sp001.infrastructure.product001_mvp1_http_codec import decode_product001_mvp1_decision
from sp001.services.product001_mvp1_execution_gate import authorization_payload


def verify_exported_commercial_receipt(
    *,
    receipt: CommercialReceiptV1,
    certificate: CommitmentCertificateV1,
    audit_sequence: int,
    canonical_audit_record: str,
    trusted_gate_id: str,
    trusted_gate_key: Ed25519PublicKey,
    trusted_issuer_id: str,
    trusted_authority_key: Ed25519PublicKey,
) -> None:
    """Verify the Gate's historical attestation and the authority certificate."""
    verify_commitment_signature(certificate, trusted_key=trusted_authority_key)
    verify_commercial_receipt(
        receipt,
        certificate=certificate,
        trusted_gate_id=trusted_gate_id,
        trusted_gate_key=trusted_gate_key,
    )
    context = certificate.context
    if context.issuer_id != trusted_issuer_id:
        raise PermissionError("unexpected commitment issuer")
    statement = receipt.statement
    if type(audit_sequence) is not int or audit_sequence != statement.audit_sequence:
        raise PermissionError("unexpected audit sequence")

    try:
        if sha256(canonical_audit_record.encode("ascii")).hexdigest() != statement.audit_digest:
            raise PermissionError("audit digest mismatch")
        audit = json.loads(canonical_audit_record)
        definition = audit["definition"]
        decision = decode_product001_mvp1_decision(json.loads(definition))
        derived_definition = json.dumps(
            asdict(decision), sort_keys=True, separators=(",", ":"),
            ensure_ascii=True, allow_nan=False,
        )
        expected = {
            "action": "RECORD_DECISION",
            "decision_id": context.operation_id,
            "grant_id": decision.authorization_grant_id,
            "definition": derived_definition,
            "commitment": {
                "version": 1,
                "certificate_digest": statement.certificate_digest,
                "context": asdict(context),
            },
        }
        canonical_expected = json.dumps(
            expected, sort_keys=True, separators=(",", ":"),
            ensure_ascii=True, allow_nan=False,
        )
        if (
            canonical_audit_record != canonical_expected
            or decision.decision_id != context.operation_id
            or decision.document_scope.organization_id != context.organization_id
            or sha256(authorization_payload(decision)).hexdigest() != context.decision_digest
        ):
            raise PermissionError("audit does not match committed decision")
    except (AttributeError, KeyError, TypeError, ValueError, RecursionError) as error:
        raise PermissionError("invalid exported audit record") from error
