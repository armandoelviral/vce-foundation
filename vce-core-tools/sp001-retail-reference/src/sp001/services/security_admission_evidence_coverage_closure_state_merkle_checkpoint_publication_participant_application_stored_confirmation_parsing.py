import json
from collections.abc import Iterable

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState,
)
from sp001.services.security_admission_portable_integer_validation import (
    validate_security_admission_positive_uint64,
)


StoredConfirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation
)
StoredState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState
)

_DOMAIN = (
    "SP001-SECURITY-ADMISSION-CLOSURE-STATE-"
    "MERKLE-CHECKPOINT-PUBLICATION-PARTICIPANT-"
    "APPLICATION-CONFIRMATION"
)
_TOP_LEVEL_KEYS = frozenset(
    (
        "decision",
        "domain",
        "participant_id",
        "publication_state",
        "storage_schema_version",
    )
)
_STATE_KEYS = frozenset(
    (
        "checkpoint_serialization",
        "phase",
        "public_key_encoding",
        "public_key_fingerprint",
        "publication_id",
        "revision",
        "signature_encoding",
        "signature_hex",
        "signing_algorithm",
        "signing_key_id",
        "storage_schema_version",
    )
)
_UINT64_WIDTH = 20


def parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation(
    *,
    serialization: str,
) -> StoredConfirmation:
    """Parse one strict canonical portable application confirmation."""

    if type(serialization) is not str:
        raise TypeError(
            "serialization must be a string"
        )
    if not serialization:
        raise ValueError(
            "serialization must not be empty"
        )

    try:
        document = json.loads(
            serialization,
            object_pairs_hook=_strict_json_object,
            parse_constant=_reject_json_constant,
        )
    except json.JSONDecodeError as error:
        raise ValueError(
            "serialization must contain valid JSON"
        ) from error

    _require_exact_keys(
        value=document,
        expected=_TOP_LEVEL_KEYS,
        field="stored confirmation",
    )

    if document["domain"] != _DOMAIN:
        raise ValueError(
            "stored confirmation domain is not supported"
        )

    state_document = document["publication_state"]
    _require_exact_keys(
        value=state_document,
        expected=_STATE_KEYS,
        field="publication_state",
    )

    stored_state = StoredState(
        storage_schema_version=(
            state_document["storage_schema_version"]
        ),
        publication_id=state_document["publication_id"],
        checkpoint_serialization=(
            state_document["checkpoint_serialization"]
        ),
        signing_key_id=state_document["signing_key_id"],
        signing_algorithm=(
            state_document["signing_algorithm"]
        ),
        public_key_encoding=(
            state_document["public_key_encoding"]
        ),
        public_key_fingerprint=(
            state_document["public_key_fingerprint"]
        ),
        signature_encoding=(
            state_document["signature_encoding"]
        ),
        signature=_decode_signature_hex(
            state_document["signature_hex"]
        ),
        phase=state_document["phase"],
        revision=_decode_uint64(
            state_document["revision"]
        ),
    )

    stored_confirmation = StoredConfirmation(
        storage_schema_version=(
            document["storage_schema_version"]
        ),
        participant_id=document["participant_id"],
        decision=document["decision"],
        publication_state=stored_state,
    )

    canonical = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation(
            stored_confirmation=stored_confirmation,
        )
    )
    if canonical != serialization:
        raise ValueError(
            "serialization must be canonical"
        )

    return stored_confirmation


def _strict_json_object(
    pairs: Iterable[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}

    for key, value in pairs:
        if key in result:
            raise ValueError(
                "serialization must not contain duplicate keys"
            )
        result[key] = value

    return result


def _reject_json_constant(
    value: str,
) -> object:
    raise ValueError(
        f"serialization contains unsupported JSON constant: {value}"
    )


def _require_exact_keys(
    *,
    value: object,
    expected: frozenset[str],
    field: str,
) -> None:
    if type(value) is not dict:
        raise TypeError(
            f"{field} must be a JSON object"
        )
    if frozenset(value) != expected:
        raise ValueError(
            f"{field} must contain exactly the supported keys"
        )


def _decode_signature_hex(
    value: object,
) -> bytes:
    if type(value) is not str:
        raise TypeError(
            "signature_hex must be a string"
        )
    if not value:
        raise ValueError(
            "signature_hex must not be empty"
        )
    if (
        len(value) % 2 != 0
        or not value.isascii()
        or any(
            character not in "0123456789abcdef"
            for character in value
        )
    ):
        raise ValueError(
            "signature_hex must use canonical lowercase hexadecimal"
        )

    signature = bytes.fromhex(value)
    if signature.hex() != value:
        raise ValueError(
            "signature_hex must use canonical lowercase hexadecimal"
        )

    return signature


def _decode_uint64(
    value: object,
) -> int:
    if (
        type(value) is not str
        or len(value) != _UINT64_WIDTH
        or not value.isascii()
        or not value.isdecimal()
    ):
        raise ValueError(
            "stored revision is not canonical"
        )

    revision = int(value)
    validate_security_admission_positive_uint64(
        value=revision,
        field="revision",
    )

    if f"{revision:0{_UINT64_WIDTH}d}" != value:
        raise ValueError(
            "stored revision is not canonical"
        )

    return revision
