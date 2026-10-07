import json

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord,
)
from sp001.services.security_admission_portable_integer_validation import (
    validate_security_admission_positive_uint64,
)


StoredDecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord
)
_DOMAIN = (
    "SP001-SECURITY-ADMISSION-CLOSURE-STATE-"
    "MERKLE-CHECKPOINT-PUBLICATION-DECISION"
)
_UINT64_WIDTH = 20


def serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record(
    *,
    stored_record: StoredDecisionRecord,
) -> str:
    """Serialize one portable decision record as strict canonical JSON."""

    if not isinstance(
        stored_record,
        StoredDecisionRecord,
    ):
        raise TypeError(
            "stored_record must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationDecisionStoredRecord"
        )

    document = {
        "decision": stored_record.decision,
        "domain": _DOMAIN,
        "participant_ids": list(
            stored_record.participant_ids
        ),
        "preparations": [
            {
                "participant_id": participant_id,
                "publication_state": {
                    "checkpoint_serialization": (
                        stored_state
                        .checkpoint_serialization
                    ),
                    "phase": stored_state.phase,
                    "public_key_encoding": (
                        stored_state
                        .public_key_encoding
                    ),
                    "public_key_fingerprint": (
                        stored_state
                        .public_key_fingerprint
                    ),
                    "publication_id": (
                        stored_state
                        .publication_id
                    ),
                    "revision": _encode_uint64(
                        stored_state.revision
                    ),
                    "signature_encoding": (
                        stored_state
                        .signature_encoding
                    ),
                    "signature_hex": (
                        stored_state
                        .signature
                        .hex()
                    ),
                    "signing_algorithm": (
                        stored_state
                        .signing_algorithm
                    ),
                    "signing_key_id": (
                        stored_state
                        .signing_key_id
                    ),
                    "storage_schema_version": (
                        stored_state
                        .storage_schema_version
                    ),
                },
            }
            for participant_id, stored_state in (
                stored_record.preparations
            )
        ],
        "publication_id": stored_record.publication_id,
        "storage_schema_version": (
            stored_record.storage_schema_version
        ),
    }

    return json.dumps(
        document,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _encode_uint64(
    value: int,
) -> str:
    validate_security_admission_positive_uint64(
        value=value,
        field="revision",
    )
    return f"{value:0{_UINT64_WIDTH}d}"
