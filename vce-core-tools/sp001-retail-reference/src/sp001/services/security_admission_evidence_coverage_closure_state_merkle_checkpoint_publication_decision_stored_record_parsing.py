import json
from collections.abc import Iterable
from typing import Never

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState,
)
from sp001.services.security_admission_portable_integer_validation import (
    validate_security_admission_positive_uint64,
)


StoredDecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord
)
StoredState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState
)
_DOMAIN = (
    "SP001-SECURITY-ADMISSION-CLOSURE-STATE-"
    "MERKLE-CHECKPOINT-PUBLICATION-DECISION"
)
_UINT64_WIDTH = 20
_TOP_LEVEL_KEYS = frozenset(
    (
        "decision",
        "domain",
        "participant_ids",
        "preparations",
        "publication_id",
        "storage_schema_version",
    )
)
_PREPARATION_KEYS = frozenset(
    (
        "participant_id",
        "publication_state",
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
_LOWERCASE_HEX = frozenset(
    "0123456789abcdef"
)


def parse_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record(
    *,
    serialization: str,
) -> StoredDecisionRecord:
    """Parse one strict canonical durable publication-decision document."""

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
        field="decision document",
    )

    if document["domain"] != _DOMAIN:
        raise ValueError(
            "decision document domain is not supported"
        )

    participant_ids_value = document[
        "participant_ids"
    ]
    if not isinstance(
        participant_ids_value,
        list,
    ):
        raise TypeError(
            "participant_ids must be a JSON array"
        )
    participant_ids = tuple(
        participant_ids_value
    )

    preparations_value = document[
        "preparations"
    ]
    if not isinstance(
        preparations_value,
        list,
    ):
        raise TypeError(
            "preparations must be a JSON array"
        )

    preparations = tuple(
        _parse_preparation(value)
        for value in preparations_value
    )

    stored_record = StoredDecisionRecord(
        storage_schema_version=(
            document["storage_schema_version"]
        ),
        publication_id=document["publication_id"],
        participant_ids=participant_ids,
        preparations=preparations,
        decision=document["decision"],
    )

    canonical = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record(
            stored_record=stored_record,
        )
    )
    if canonical != serialization:
        raise ValueError(
            "serialization must be canonical"
        )

    return stored_record


def _parse_preparation(
    value: object,
) -> tuple[str, StoredState]:
    _require_exact_keys(
        value=value,
        expected=_PREPARATION_KEYS,
        field="preparation",
    )

    state_value = value["publication_state"]
    _require_exact_keys(
        value=state_value,
        expected=_STATE_KEYS,
        field="publication_state",
    )

    signature = _decode_signature_hex(
        state_value["signature_hex"]
    )
    revision = _decode_uint64(
        state_value["revision"]
    )

    stored_state = StoredState(
        storage_schema_version=(
            state_value["storage_schema_version"]
        ),
        publication_id=state_value["publication_id"],
        checkpoint_serialization=(
            state_value["checkpoint_serialization"]
        ),
        signing_key_id=(
            state_value["signing_key_id"]
        ),
        signing_algorithm=(
            state_value["signing_algorithm"]
        ),
        public_key_encoding=(
            state_value["public_key_encoding"]
        ),
        public_key_fingerprint=(
            state_value["public_key_fingerprint"]
        ),
        signature_encoding=(
            state_value["signature_encoding"]
        ),
        signature=signature,
        phase=state_value["phase"],
        revision=revision,
    )

    return (
        value["participant_id"],
        stored_state,
    )


def _decode_signature_hex(
    value: object,
) -> bytes:
    if type(value) is not str:
        raise TypeError(
            "signature_hex must be a string"
        )
    if (
        not value
        or len(value) % 2 != 0
        or any(
            character not in _LOWERCASE_HEX
            for character in value
        )
    ):
        raise ValueError(
            "signature_hex must contain canonical "
            "lowercase hexadecimal bytes"
        )

    return bytes.fromhex(value)


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
            "revision must use canonical uint64 encoding"
        )

    revision = int(value)
    validate_security_admission_positive_uint64(
        value=revision,
        field="revision",
    )

    if f"{revision:0{_UINT64_WIDTH}d}" != value:
        raise ValueError(
            "revision must use canonical uint64 encoding"
        )

    return revision


def _require_exact_keys(
    *,
    value: object,
    expected: frozenset[str],
    field: str,
) -> None:
    if not isinstance(value, dict):
        raise TypeError(
            f"{field} must be a JSON object"
        )
    if frozenset(value) != expected:
        raise ValueError(
            f"{field} must contain exact canonical keys"
        )


def _strict_json_object(
    pairs: Iterable[tuple[str, object]],
) -> dict[str, object]:
    value: dict[str, object] = {}

    for key, member in pairs:
        if key in value:
            raise ValueError(
                "serialization must not contain "
                "duplicate JSON object keys"
            )
        value[key] = member

    return value


def _reject_json_constant(
    value: str,
) -> Never:
    raise ValueError(
        f"JSON constant {value!r} is not supported"
    )
