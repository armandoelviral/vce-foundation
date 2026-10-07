import json

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent,
)


StoredIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent
)
_DOMAIN = (
    "SP001-SECURITY-ADMISSION-CLOSURE-STATE-"
    "MERKLE-CHECKPOINT-PUBLICATION-INTENT"
)


def serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
    *,
    stored_intent: StoredIntent,
) -> str:
    """Serialize one portable signed publication intent canonically."""

    if not isinstance(
        stored_intent,
        StoredIntent,
    ):
        raise TypeError(
            "stored_intent must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationStoredIntent"
        )

    document = {
        "checkpoint_serialization": (
            stored_intent.checkpoint_serialization
        ),
        "domain": _DOMAIN,
        "public_key_encoding": (
            stored_intent.public_key_encoding
        ),
        "public_key_fingerprint": (
            stored_intent.public_key_fingerprint
        ),
        "publication_id": (
            stored_intent.publication_id
        ),
        "signature_encoding": (
            stored_intent.signature_encoding
        ),
        "signature_hex": (
            stored_intent.signature.hex()
        ),
        "signing_algorithm": (
            stored_intent.signing_algorithm
        ),
        "signing_key_id": (
            stored_intent.signing_key_id
        ),
        "storage_schema_version": (
            stored_intent.storage_schema_version
        ),
    }

    return json.dumps(
        document,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
