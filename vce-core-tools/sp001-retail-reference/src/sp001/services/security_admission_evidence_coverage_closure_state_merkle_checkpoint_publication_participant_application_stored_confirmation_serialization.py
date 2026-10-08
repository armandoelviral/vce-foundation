import json

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation,
)
from sp001.services.security_admission_portable_integer_validation import (
    validate_security_admission_positive_uint64,
)


StoredConfirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation
)
_DOMAIN = (
    "SP001-SECURITY-ADMISSION-CLOSURE-STATE-"
    "MERKLE-CHECKPOINT-PUBLICATION-PARTICIPANT-"
    "APPLICATION-CONFIRMATION"
)
_UINT64_WIDTH = 20


def serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation(
    *,
    stored_confirmation: StoredConfirmation,
) -> str:
    """Serialize one portable application confirmation as canonical JSON."""

    if not isinstance(
        stored_confirmation,
        StoredConfirmation,
    ):
        raise TypeError(
            "stored_confirmation must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationParticipant"
            "ApplicationStoredConfirmation"
        )

    stored_state = (
        stored_confirmation.publication_state
    )

    document = {
        "decision": stored_confirmation.decision,
        "domain": _DOMAIN,
        "participant_id": (
            stored_confirmation.participant_id
        ),
        "publication_state": {
            "checkpoint_serialization": (
                stored_state.checkpoint_serialization
            ),
            "phase": stored_state.phase,
            "public_key_encoding": (
                stored_state.public_key_encoding
            ),
            "public_key_fingerprint": (
                stored_state.public_key_fingerprint
            ),
            "publication_id": (
                stored_state.publication_id
            ),
            "revision": _encode_uint64(
                stored_state.revision
            ),
            "signature_encoding": (
                stored_state.signature_encoding
            ),
            "signature_hex": (
                stored_state.signature.hex()
            ),
            "signing_algorithm": (
                stored_state.signing_algorithm
            ),
            "signing_key_id": (
                stored_state.signing_key_id
            ),
            "storage_schema_version": (
                stored_state.storage_schema_version
            ),
        },
        "storage_schema_version": (
            stored_confirmation.storage_schema_version
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
