import inspect
from dataclasses import replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet,
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
DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
StoredDecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord
)
PreparationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet
)
project_decision = (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record
)
project_state = (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state
)


def create_decision_record(
    *,
    size: int = 3,
    decision: Decision = Decision.COMMIT,
) -> DecisionRecord:
    (
        publication_intent,
        participant_set,
        preparation_set,
    ) = create_components(
        size=size,
    )

    return DecisionRecord(
        publication_intent=publication_intent,
        participant_set=participant_set,
        preparation_set=preparation_set,
        decision=decision,
    )


@pytest.mark.parametrize(
    "decision",
    tuple(Decision),
)
def test_projection_returns_nominal_stored_record(
    decision: Decision,
) -> None:
    projected = project_decision(
        decision_record=create_decision_record(
            decision=decision,
        ),
    )

    assert isinstance(
        projected,
        StoredDecisionRecord,
    )


@pytest.mark.parametrize(
    "decision",
    tuple(Decision),
)
def test_projection_preserves_exact_decision_value(
    decision: Decision,
) -> None:
    projected = project_decision(
        decision_record=create_decision_record(
            decision=decision,
        ),
    )

    assert projected.decision == decision.value
    assert type(projected.decision) is str


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        3,
        5,
        8,
    ),
)
def test_projection_preserves_canonical_participant_ids(
    size: int,
) -> None:
    record = create_decision_record(
        size=size,
    )

    projected = project_decision(
        decision_record=record,
    )

    assert projected.participant_ids == tuple(
        participant.participant_id
        for participant in (
            record
            .participant_set
            .participants
        )
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
def test_projection_preserves_each_preparation(
    size: int,
) -> None:
    record = create_decision_record(
        size=size,
    )

    projected = project_decision(
        decision_record=record,
    )

    assert projected.preparations == tuple(
        (
            preparation.participant_id,
            project_state(
                state=preparation.publication_state,
            ),
        )
        for preparation in (
            record
            .preparation_set
            .preparations
        )
    )


def test_projection_preserves_publication_id() -> None:
    record = create_decision_record()

    projected = project_decision(
        decision_record=record,
    )

    assert (
        projected.publication_id
        == record.publication_intent.publication_id
    )


def test_projection_uses_storage_schema_version_one() -> None:
    projected = project_decision(
        decision_record=create_decision_record(),
    )

    assert projected.storage_schema_version == 1
    assert type(projected.storage_schema_version) is int


def test_projection_is_deterministic_for_same_record() -> None:
    record = create_decision_record()

    first = project_decision(
        decision_record=record,
    )
    second = project_decision(
        decision_record=record,
    )

    assert first == second


def test_projection_does_not_retain_participant_objects() -> None:
    record = create_decision_record()

    projected = project_decision(
        decision_record=record,
    )

    assert all(
        type(participant_id) is str
        for participant_id in projected.participant_ids
    )
    assert all(
        participant
        not in projected.participant_ids
        for participant in (
            record
            .participant_set
            .participants
        )
    )


def test_projection_does_not_retain_runtime_states() -> None:
    record = create_decision_record()

    projected = project_decision(
        decision_record=record,
    )

    runtime_states = tuple(
        preparation.publication_state
        for preparation in (
            record
            .preparation_set
            .preparations
        )
    )
    stored_states = tuple(
        stored_state
        for _, stored_state in projected.preparations
    )

    assert all(
        runtime_state not in stored_states
        for runtime_state in runtime_states
    )


def test_abort_projection_preserves_incomplete_evidence() -> None:
    record = create_decision_record(
        decision=Decision.ABORT,
    )
    incomplete_set = PreparationSet(
        preparations=(
            record
            .preparation_set
            .preparations[:1]
        ),
    )
    incomplete_record = replace(
        record,
        preparation_set=incomplete_set,
    )

    projected = project_decision(
        decision_record=incomplete_record,
    )

    assert projected.decision == "ABORT"
    assert len(projected.participant_ids) == 3
    assert len(projected.preparations) == 1


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "decision-record",
        1,
        True,
        (),
    ),
)
def test_projection_rejects_invalid_record_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="decision_record",
    ):
        project_decision(
            decision_record=value,
        )


def test_projection_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        project_decision
    )

    assert tuple(signature.parameters) == (
        "decision_record",
    )
    parameter = signature.parameters[
        "decision_record"
    ]
    assert (
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
    )
    assert parameter.annotation is DecisionRecord
    assert (
        signature.return_annotation
        is StoredDecisionRecord
    )


def test_projection_defines_no_serialization_persistence_or_effects() -> None:
    source = inspect.getsource(
        project_decision
    ).lower()

    for forbidden in (
        "json.",
        "serialize",
        "deserialize",
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
