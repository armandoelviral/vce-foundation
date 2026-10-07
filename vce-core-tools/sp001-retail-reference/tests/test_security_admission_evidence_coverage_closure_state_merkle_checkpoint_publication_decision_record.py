import inspect
from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    create_intent,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation import (
    create_preparation,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    create_set as create_participant_set,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
PreparationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet
)


def create_components(
    *,
    size: int = 3,
):
    base_preparation = create_preparation(
        participant_id="participant-001",
    )
    preparation_set = PreparationSet(
        preparations=tuple(
            replace(
                base_preparation,
                participant_id=f"participant-{index:03d}",
            )
            for index in range(1, size + 1)
        ),
    )
    publication_intent = (
        base_preparation
        .publication_state
        .publication_intent
    )
    participant_set = create_participant_set(
        size=size,
    )

    return (
        publication_intent,
        participant_set,
        preparation_set,
    )


def create_record(
    *,
    decision: Decision = Decision.COMMIT,
) -> DecisionRecord:
    (
        publication_intent,
        participant_set,
        preparation_set,
    ) = create_components()

    return DecisionRecord(
        publication_intent=publication_intent,
        participant_set=participant_set,
        preparation_set=preparation_set,
        decision=decision,
    )


def test_record_has_exact_fields() -> None:
    assert tuple(
        field.name
        for field in fields(DecisionRecord)
    ) == (
        "publication_intent",
        "participant_set",
        "preparation_set",
        "decision",
    )


@pytest.mark.parametrize(
    "decision",
    tuple(Decision),
)
def test_record_preserves_exact_evidence_references(
    decision: Decision,
) -> None:
    (
        publication_intent,
        participant_set,
        preparation_set,
    ) = create_components()

    record = DecisionRecord(
        publication_intent=publication_intent,
        participant_set=participant_set,
        preparation_set=preparation_set,
        decision=decision,
    )

    assert record.publication_intent is publication_intent
    assert record.participant_set is participant_set
    assert record.preparation_set is preparation_set
    assert record.decision is decision


@pytest.mark.parametrize(
    "decision",
    tuple(Decision),
)
def test_each_nominal_decision_can_be_recorded(
    decision: Decision,
) -> None:
    assert create_record(
        decision=decision,
    ).decision is decision


def test_record_is_frozen() -> None:
    record = create_record()

    with pytest.raises(FrozenInstanceError):
        record.decision = Decision.ABORT


def test_record_uses_slots() -> None:
    assert not hasattr(create_record(), "__dict__")


def test_equal_values_are_equal() -> None:
    (
        publication_intent,
        participant_set,
        preparation_set,
    ) = create_components()

    first = DecisionRecord(
        publication_intent=publication_intent,
        participant_set=participant_set,
        preparation_set=preparation_set,
        decision=Decision.COMMIT,
    )
    second = DecisionRecord(
        publication_intent=publication_intent,
        participant_set=participant_set,
        preparation_set=preparation_set,
        decision=Decision.COMMIT,
    )

    assert first == second


def test_different_decisions_are_not_equal() -> None:
    record = create_record(
        decision=Decision.COMMIT,
    )

    assert record != replace(
        record,
        decision=Decision.ABORT,
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "publication-intent",
        1,
        True,
        (),
    ),
)
def test_publication_intent_rejects_invalid_type(
    value: object,
) -> None:
    record = create_record()

    with pytest.raises(
        TypeError,
        match="publication_intent",
    ):
        replace(
            record,
            publication_intent=value,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "participant-set",
        1,
        True,
        (),
    ),
)
def test_participant_set_rejects_invalid_type(
    value: object,
) -> None:
    record = create_record()

    with pytest.raises(
        TypeError,
        match="participant_set",
    ):
        replace(
            record,
            participant_set=value,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "preparation-set",
        1,
        True,
        (),
    ),
)
def test_preparation_set_rejects_invalid_type(
    value: object,
) -> None:
    record = create_record()

    with pytest.raises(
        TypeError,
        match="preparation_set",
    ):
        replace(
            record,
            preparation_set=value,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "COMMIT",
        "ABORT",
        1,
        True,
        (),
    ),
)
def test_decision_rejects_invalid_type(
    value: object,
) -> None:
    record = create_record()

    with pytest.raises(
        TypeError,
        match="decision",
    ):
        replace(
            record,
            decision=value,
        )


def test_preparation_from_other_publication_is_rejected() -> None:
    record = create_record()
    other_intent = create_intent(
        publication_id="publication-other",
        scalar=2,
    )

    with pytest.raises(
        ValueError,
        match="exact publication intent",
    ):
        replace(
            record,
            publication_intent=other_intent,
        )


def test_every_preparation_retains_recorded_intent() -> None:
    record = create_record()

    assert all(
        preparation.publication_state.publication_intent
        == record.publication_intent
        for preparation in record.preparation_set.preparations
    )


def test_record_does_not_derive_a_decision() -> None:
    source = inspect.getsource(DecisionRecord)

    assert "verify_security_admission" not in source
    assert "return Decision.COMMIT" not in source
    assert "return Decision.ABORT" not in source


def test_record_defines_no_persistence_or_participant_effects() -> None:
    source = inspect.getsource(DecisionRecord).lower()

    for forbidden in (
        "sqlite",
        "database",
        "compare_and_swap",
        ".prepare(",
        ".commit(",
        ".abort(",
        "network",
        "http",
        "socket",
    ):
        assert forbidden not in source
