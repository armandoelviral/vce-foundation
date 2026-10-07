import inspect
from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    create_components,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
StoredDecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord
)
project_state = (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state
)
UINT64_MAX = (1 << 64) - 1


def create_stored_record(
    *,
    size: int = 3,
    storage_schema_version: int = 1,
    decision: str = "COMMIT",
) -> StoredDecisionRecord:
    (
        publication_intent,
        participant_set,
        preparation_set,
    ) = create_components(
        size=size,
    )

    participant_ids = tuple(
        participant.participant_id
        for participant in participant_set.participants
    )
    preparations = tuple(
        (
            preparation.participant_id,
            project_state(
                state=preparation.publication_state,
            ),
        )
        for preparation in preparation_set.preparations
    )

    return StoredDecisionRecord(
        storage_schema_version=storage_schema_version,
        publication_id=publication_intent.publication_id,
        participant_ids=participant_ids,
        preparations=preparations,
        decision=decision,
    )


def test_stored_record_has_exact_fields() -> None:
    assert tuple(
        field.name
        for field in fields(StoredDecisionRecord)
    ) == (
        "storage_schema_version",
        "publication_id",
        "participant_ids",
        "preparations",
        "decision",
    )


@pytest.mark.parametrize(
    "decision",
    (
        "COMMIT",
        "ABORT",
    ),
)
def test_supported_decision_is_preserved(
    decision: str,
) -> None:
    record = create_stored_record(
        decision=decision,
    )

    assert record.decision == decision
    assert type(record.decision) is str


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        3,
        5,
    ),
)
def test_canonical_participant_graph_is_preserved(
    size: int,
) -> None:
    record = create_stored_record(
        size=size,
    )

    expected_ids = tuple(
        f"participant-{index:03d}"
        for index in range(1, size + 1)
    )

    assert record.participant_ids == expected_ids
    assert tuple(
        participant_id
        for participant_id, _ in record.preparations
    ) == expected_ids


def test_stored_record_is_frozen() -> None:
    record = create_stored_record()

    with pytest.raises(FrozenInstanceError):
        record.decision = "ABORT"


def test_stored_record_uses_slots() -> None:
    assert not hasattr(
        create_stored_record(),
        "__dict__",
    )


def test_equal_values_are_equal() -> None:
    record = create_stored_record()

    assert record == replace(record)


@pytest.mark.parametrize(
    "value",
    (
        1,
        2,
        UINT64_MAX,
    ),
)
def test_storage_schema_version_accepts_positive_uint64(
    value: int,
) -> None:
    assert create_stored_record(
        storage_schema_version=value,
    ).storage_schema_version == value


@pytest.mark.parametrize(
    "value",
    (
        0,
        -1,
        UINT64_MAX + 1,
    ),
)
def test_storage_schema_version_rejects_out_of_range_value(
    value: int,
) -> None:
    with pytest.raises(ValueError):
        create_stored_record(
            storage_schema_version=value,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        True,
        False,
        1.0,
        "1",
        object(),
    ),
)
def test_storage_schema_version_requires_exact_integer(
    value: object,
) -> None:
    with pytest.raises(TypeError):
        create_stored_record(
            storage_schema_version=value,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        b"publication-001",
        1,
        True,
        object(),
    ),
)
def test_publication_id_rejects_invalid_type(
    value: object,
) -> None:
    record = create_stored_record()

    with pytest.raises(
        TypeError,
        match="publication_id",
    ):
        replace(
            record,
            publication_id=value,
        )


def test_publication_id_rejects_empty_value() -> None:
    record = create_stored_record()

    with pytest.raises(
        ValueError,
        match="publication_id",
    ):
        replace(
            record,
            publication_id="",
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        [],
        "participant-001",
        object(),
    ),
)
def test_participant_ids_requires_tuple(
    value: object,
) -> None:
    record = create_stored_record()

    with pytest.raises(
        TypeError,
        match="participant_ids",
    ):
        replace(
            record,
            participant_ids=value,
        )


def test_participant_ids_rejects_empty_tuple() -> None:
    record = create_stored_record()

    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        replace(
            record,
            participant_ids=(),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        b"participant-001",
        1,
        True,
        object(),
    ),
)
def test_participant_ids_rejects_non_string_member(
    value: object,
) -> None:
    record = create_stored_record()

    with pytest.raises(
        TypeError,
        match="only strings",
    ):
        replace(
            record,
            participant_ids=(
                value,
            ),
        )


def test_participant_ids_rejects_empty_member() -> None:
    record = create_stored_record()

    with pytest.raises(
        ValueError,
        match="empty values",
    ):
        replace(
            record,
            participant_ids=(
                "",
            ),
        )


def test_participant_ids_rejects_duplicate_member() -> None:
    record = create_stored_record()

    with pytest.raises(
        ValueError,
        match="unique",
    ):
        replace(
            record,
            participant_ids=(
                "participant-001",
                "participant-001",
            ),
        )


def test_participant_ids_rejects_noncanonical_order() -> None:
    record = create_stored_record()

    with pytest.raises(
        ValueError,
        match="canonical order",
    ):
        replace(
            record,
            participant_ids=tuple(
                reversed(record.participant_ids)
            ),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        [],
        "preparations",
        object(),
    ),
)
def test_preparations_requires_tuple(
    value: object,
) -> None:
    record = create_stored_record()

    with pytest.raises(
        TypeError,
        match="preparations",
    ):
        replace(
            record,
            preparations=value,
        )


def test_preparations_rejects_empty_tuple() -> None:
    record = create_stored_record()

    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        replace(
            record,
            preparations=(),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        (),
        ("participant-001",),
        ("participant-001", object(), "extra"),
        ["participant-001", object()],
    ),
)
def test_preparations_rejects_invalid_pair_shape(
    value: object,
) -> None:
    record = create_stored_record()

    with pytest.raises(
        TypeError,
        match="tuples",
    ):
        replace(
            record,
            preparations=(
                value,
            ),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        b"participant-001",
        1,
        True,
        object(),
    ),
)
def test_preparation_participant_id_requires_string(
    value: object,
) -> None:
    record = create_stored_record()
    _, stored_state = record.preparations[0]

    with pytest.raises(
        TypeError,
        match="participant_id",
    ):
        replace(
            record,
            preparations=(
                (
                    value,
                    stored_state,
                ),
            ),
        )


def test_preparation_participant_id_rejects_empty_value() -> None:
    record = create_stored_record()
    _, stored_state = record.preparations[0]

    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        replace(
            record,
            preparations=(
                (
                    "",
                    stored_state,
                ),
            ),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "stored-state",
        1,
        True,
        (),
    ),
)
def test_preparation_rejects_invalid_stored_state(
    value: object,
) -> None:
    record = create_stored_record()

    with pytest.raises(
        TypeError,
        match="stored_state",
    ):
        replace(
            record,
            preparations=(
                (
                    "participant-001",
                    value,
                ),
            ),
        )


def test_preparation_rejects_other_publication() -> None:
    record = create_stored_record()
    participant_id, stored_state = (
        record.preparations[0]
    )
    changed_state = replace(
        stored_state,
        publication_id="publication-other",
    )

    with pytest.raises(
        ValueError,
        match="recorded publication_id",
    ):
        replace(
            record,
            preparations=(
                (
                    participant_id,
                    changed_state,
                ),
            ),
        )


def test_preparations_reject_duplicate_participant() -> None:
    record = create_stored_record()
    first = record.preparations[0]

    with pytest.raises(
        ValueError,
        match="unique",
    ):
        replace(
            record,
            preparations=(
                first,
                first,
            ),
        )


def test_preparations_reject_noncanonical_order() -> None:
    record = create_stored_record()

    with pytest.raises(
        ValueError,
        match="canonical",
    ):
        replace(
            record,
            preparations=tuple(
                reversed(record.preparations)
            ),
        )


def test_abort_may_preserve_incomplete_preparation_evidence() -> None:
    record = create_stored_record(
        decision="ABORT",
    )

    incomplete = replace(
        record,
        preparations=record.preparations[:1],
    )

    assert incomplete.decision == "ABORT"
    assert len(incomplete.preparations) == 1
    assert len(incomplete.participant_ids) == 3


@pytest.mark.parametrize(
    "value",
    (
        None,
        Decision.COMMIT,
        b"COMMIT",
        1,
        True,
        object(),
    ),
)
def test_decision_requires_plain_string(
    value: object,
) -> None:
    record = create_stored_record()

    with pytest.raises(
        TypeError,
        match="decision",
    ):
        replace(
            record,
            decision=value,
        )


@pytest.mark.parametrize(
    "value",
    (
        "",
        "commit",
        "abort",
        "COMMITTED",
        "ABORTED",
        "PREPARED",
    ),
)
def test_decision_rejects_unsupported_value(
    value: str,
) -> None:
    record = create_stored_record()

    with pytest.raises(
        ValueError,
        match="supported",
    ):
        replace(
            record,
            decision=value,
        )


def test_stored_record_defines_no_projection_or_deserialization() -> None:
    source = inspect.getsource(
        StoredDecisionRecord
    ).lower()

    for forbidden in (
        "serialize",
        "deserialize",
        "json.",
        "sqlite",
        "database",
        "participant.prepare",
        "participant.commit",
        "participant.abort",
    ):
        assert forbidden not in source
