import inspect
import json
from dataclasses import replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record import (
    create_stored_record,
)


StoredDecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord
)
serialize = (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record
)
DOMAIN = (
    "SP001-SECURITY-ADMISSION-CLOSURE-STATE-"
    "MERKLE-CHECKPOINT-PUBLICATION-DECISION"
)
UINT64_MAX = (1 << 64) - 1
TOP_LEVEL_KEYS = {
    "decision",
    "domain",
    "participant_ids",
    "preparations",
    "publication_id",
    "storage_schema_version",
}
PREPARATION_KEYS = {
    "participant_id",
    "publication_state",
}
STATE_KEYS = {
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
}


def document(
    *,
    size: int = 3,
    decision: str = "COMMIT",
):
    stored_record = create_stored_record(
        size=size,
        decision=decision,
    )
    serialized = serialize(
        stored_record=stored_record,
    )

    return (
        stored_record,
        serialized,
        json.loads(serialized),
    )


def test_serialization_returns_plain_string() -> None:
    _, serialized, _ = document()

    assert type(serialized) is str


@pytest.mark.parametrize(
    "decision",
    (
        "COMMIT",
        "ABORT",
    ),
)
def test_serialization_preserves_decision(
    decision: str,
) -> None:
    _, _, value = document(
        decision=decision,
    )

    assert value["decision"] == decision


def test_serialization_uses_exact_domain() -> None:
    _, _, value = document()

    assert value["domain"] == DOMAIN


def test_serialization_has_exact_top_level_keys() -> None:
    _, _, value = document()

    assert set(value) == TOP_LEVEL_KEYS


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        3,
        5,
    ),
)
def test_serialization_preserves_participant_ids(
    size: int,
) -> None:
    stored_record, _, value = document(
        size=size,
    )

    assert value["participant_ids"] == list(
        stored_record.participant_ids
    )


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        3,
        5,
    ),
)
def test_serialization_preserves_preparation_order(
    size: int,
) -> None:
    stored_record, _, value = document(
        size=size,
    )

    assert tuple(
        preparation["participant_id"]
        for preparation in value["preparations"]
    ) == tuple(
        participant_id
        for participant_id, _ in (
            stored_record.preparations
        )
    )


def test_serialization_has_exact_preparation_keys() -> None:
    _, _, value = document()

    assert all(
        set(preparation) == PREPARATION_KEYS
        for preparation in value["preparations"]
    )


def test_serialization_has_exact_state_keys() -> None:
    _, _, value = document()

    assert all(
        set(preparation["publication_state"])
        == STATE_KEYS
        for preparation in value["preparations"]
    )


def test_serialization_preserves_each_stored_state() -> None:
    stored_record, _, value = document()

    for (
        participant_id,
        stored_state,
    ), serialized_preparation in zip(
        stored_record.preparations,
        value["preparations"],
        strict=True,
    ):
        state = serialized_preparation[
            "publication_state"
        ]

        assert (
            serialized_preparation["participant_id"]
            == participant_id
        )
        assert (
            state["checkpoint_serialization"]
            == stored_state.checkpoint_serialization
        )
        assert state["phase"] == stored_state.phase
        assert (
            state["public_key_encoding"]
            == stored_state.public_key_encoding
        )
        assert (
            state["public_key_fingerprint"]
            == stored_state.public_key_fingerprint
        )
        assert (
            state["publication_id"]
            == stored_state.publication_id
        )
        assert (
            state["signature_encoding"]
            == stored_state.signature_encoding
        )
        assert (
            state["signing_algorithm"]
            == stored_state.signing_algorithm
        )
        assert (
            state["signing_key_id"]
            == stored_state.signing_key_id
        )
        assert (
            state["storage_schema_version"]
            == stored_state.storage_schema_version
        )


def test_signature_is_lowercase_hex_and_round_trips() -> None:
    stored_record, _, value = document()

    for (
        _,
        stored_state,
    ), serialized_preparation in zip(
        stored_record.preparations,
        value["preparations"],
        strict=True,
    ):
        signature_hex = serialized_preparation[
            "publication_state"
        ]["signature_hex"]

        assert signature_hex == signature_hex.lower()
        assert bytes.fromhex(
            signature_hex
        ) == stored_state.signature


@pytest.mark.parametrize(
    ("revision", "expected"),
    (
        (1, "00000000000000000001"),
        (2, "00000000000000000002"),
        (999, "00000000000000000999"),
        (
            UINT64_MAX,
            "18446744073709551615",
        ),
    ),
)
def test_revision_uses_exact_twenty_digit_encoding(
    revision: int,
    expected: str,
) -> None:
    stored_record = create_stored_record(
        size=1,
    )
    participant_id, stored_state = (
        stored_record.preparations[0]
    )
    changed = replace(
        stored_record,
        preparations=(
            (
                participant_id,
                replace(
                    stored_state,
                    revision=revision,
                ),
            ),
        ),
    )

    value = json.loads(
        serialize(
            stored_record=changed,
        )
    )

    assert (
        value["preparations"][0]
        ["publication_state"]["revision"]
        == expected
    )


def test_uint64_max_is_not_encoded_as_json_number() -> None:
    stored_record = create_stored_record(
        size=1,
    )
    participant_id, stored_state = (
        stored_record.preparations[0]
    )
    changed = replace(
        stored_record,
        preparations=(
            (
                participant_id,
                replace(
                    stored_state,
                    revision=UINT64_MAX,
                ),
            ),
        ),
    )

    serialized = serialize(
        stored_record=changed,
    )

    assert (
        '"revision":"18446744073709551615"'
        in serialized
    )
    assert (
        '"revision":18446744073709551615'
        not in serialized
    )


def test_serialization_is_deterministic() -> None:
    stored_record = create_stored_record()

    assert serialize(
        stored_record=stored_record,
    ) == serialize(
        stored_record=stored_record,
    )


def test_serialization_is_canonical_json() -> None:
    _, serialized, value = document()

    assert serialized == json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def test_serialization_contains_no_insignificant_whitespace() -> None:
    _, serialized, _ = document()

    assert "\n" not in serialized
    assert ": " not in serialized
    assert ", " not in serialized


def test_serialization_escapes_non_ascii_values() -> None:
    stored_record = create_stored_record()
    changed = replace(
        stored_record,
        publication_id="publicación-001",
        preparations=tuple(
            (
                participant_id,
                replace(
                    stored_state,
                    publication_id="publicación-001",
                ),
            )
            for participant_id, stored_state in (
                stored_record.preparations
            )
        ),
    )

    serialized = serialize(
        stored_record=changed,
    )

    assert "ó" not in serialized
    assert "\\u00f3" in serialized


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "stored-record",
        1,
        True,
        (),
    ),
)
def test_serialization_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="stored_record",
    ):
        serialize(
            stored_record=value,
        )


def test_serialization_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        serialize
    )

    assert tuple(signature.parameters) == (
        "stored_record",
    )
    parameter = signature.parameters[
        "stored_record"
    ]
    assert (
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
    )
    assert parameter.annotation is StoredDecisionRecord
    assert signature.return_annotation is str


def test_serialization_defines_no_deserialization_or_persistence() -> None:
    source = inspect.getsource(
        serialize
    ).lower()

    for forbidden in (
        "json.loads",
        "deserialize",
        "sqlite",
        "database",
        "open(",
        "write(",
        "network",
        "http",
        "socket",
        "pickle",
    ):
        assert forbidden not in source
