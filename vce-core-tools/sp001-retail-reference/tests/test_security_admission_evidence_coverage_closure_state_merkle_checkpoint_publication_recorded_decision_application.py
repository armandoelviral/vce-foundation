import inspect
from dataclasses import replace
from typing import get_type_hints

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_derivation import (
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_recorded_decision_application import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationRecordedDecisionApplicationError,
    apply_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_recorded_decision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    create_intent,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
DecisionRecordStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore
)
ParticipantPreparation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation
)
ParticipantPreparationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet
)
ParticipantSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet
)
Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
PublicationState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
)
ApplicationError = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationRecordedDecisionApplicationError
)


class Participant:
    def __init__(
        self,
        *,
        participant_id: str,
        commit_results: list[object],
        abort_results: list[object],
        events: list[str] | None = None,
    ) -> None:
        self._participant_id = participant_id
        self.commit_results = commit_results
        self.abort_results = abort_results
        self.events = events
        self.prepare_calls = 0
        self.commit_calls: list[str] = []
        self.abort_calls: list[str] = []

    @property
    def participant_id(self) -> str:
        return self._participant_id

    def prepare(
        self,
        *,
        publication_intent,
    ) -> PublicationState:
        self.prepare_calls += 1
        raise AssertionError(
            "recorded decision application must not prepare"
        )

    def commit(
        self,
        *,
        publication_id: str,
    ) -> PublicationState:
        self.commit_calls.append(publication_id)
        if self.events is not None:
            self.events.append(
                f"commit:{self.participant_id}"
            )
        return self._next(self.commit_results)

    def abort(
        self,
        *,
        publication_id: str,
    ) -> PublicationState:
        self.abort_calls.append(publication_id)
        if self.events is not None:
            self.events.append(
                f"abort:{self.participant_id}"
            )
        return self._next(self.abort_results)

    @staticmethod
    def _next(
        results: list[object],
    ) -> PublicationState:
        if not results:
            raise AssertionError(
                "participant response sequence exhausted"
            )

        result = results.pop(0)
        if isinstance(result, BaseException):
            raise result
        return result


class Store:
    def __init__(
        self,
        *,
        retained: object,
        events: list[str] | None = None,
    ) -> None:
        self.retained = retained
        self.events = events
        self.read_calls: list[str] = []
        self.create_calls = 0

    def read(
        self,
        *,
        publication_id: str,
    ) -> DecisionRecord | None:
        self.read_calls.append(publication_id)
        if self.events is not None:
            self.events.append("read")
        return self.retained

    def create(
        self,
        *,
        decision_record: DecisionRecord,
    ) -> bool:
        self.create_calls += 1
        raise AssertionError(
            "application must not create decisions"
        )


class IncompleteStore:
    pass


def state(
    *,
    publication_intent,
    phase: Phase,
) -> PublicationState:
    return PublicationState(
        publication_intent=publication_intent,
        phase=phase,
        revision=4,
    )


def participant(
    index: int,
    *,
    publication_intent,
    commit_results: list[object] | None = None,
    abort_results: list[object] | None = None,
    events: list[str] | None = None,
) -> Participant:
    if commit_results is None:
        commit_results = [
            state(
                publication_intent=publication_intent,
                phase=Phase.COMMITTED,
            )
        ]
    if abort_results is None:
        abort_results = [
            state(
                publication_intent=publication_intent,
                phase=Phase.ABORTED,
            )
        ]

    return Participant(
        participant_id=f"participant-{index:03d}",
        commit_results=commit_results,
        abort_results=abort_results,
        events=events,
    )


def participant_set(
    *participants: Participant,
) -> ParticipantSet:
    return ParticipantSet(
        participants=participants,
    )


def decision_record(
    *,
    publication_intent,
    participants: ParticipantSet,
    prepared_ids: tuple[str, ...],
) -> DecisionRecord:
    preparations = tuple(
        ParticipantPreparation(
            participant_id=participant_id,
            publication_state=state(
                publication_intent=publication_intent,
                phase=Phase.PREPARED,
            ),
        )
        for participant_id in prepared_ids
    )

    return (
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision(
            publication_intent=publication_intent,
            participant_set=participants,
            preparation_set=ParticipantPreparationSet(
                preparations=preparations,
            ),
        )
    )


def apply(
    *,
    store: DecisionRecordStore,
    publication_id: str,
) -> tuple[PublicationState, ...]:
    return (
        apply_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_recorded_decision(
            decision_record_store=store,
            publication_id=publication_id,
        )
    )


def test_commit_is_applied_to_every_canonical_participant() -> None:
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
    )
    second = participant(
        2,
        publication_intent=intent,
    )
    participants = participant_set(
        first,
        second,
    )
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        prepared_ids=(
            first.participant_id,
            second.participant_id,
        ),
    )

    result = apply(
        store=Store(retained=retained),
        publication_id=intent.publication_id,
    )

    assert tuple(
        value.phase
        for value in result
    ) == (
        Phase.COMMITTED,
        Phase.COMMITTED,
    )
    assert first.commit_calls == [
        intent.publication_id,
    ]
    assert second.commit_calls == [
        intent.publication_id,
    ]
    assert first.abort_calls == []
    assert second.abort_calls == []


def test_abort_targets_only_participants_with_preparation_evidence() -> None:
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
    )
    second = participant(
        2,
        publication_intent=intent,
    )
    third = participant(
        3,
        publication_intent=intent,
    )
    participants = participant_set(
        first,
        second,
        third,
    )
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        prepared_ids=(
            first.participant_id,
            third.participant_id,
        ),
    )

    result = apply(
        store=Store(retained=retained),
        publication_id=intent.publication_id,
    )

    assert tuple(
        value.phase
        for value in result
    ) == (
        Phase.ABORTED,
        Phase.ABORTED,
    )
    assert first.abort_calls == [
        intent.publication_id,
    ]
    assert second.abort_calls == []
    assert third.abort_calls == [
        intent.publication_id,
    ]
    assert first.commit_calls == []
    assert second.commit_calls == []
    assert third.commit_calls == []


def test_zero_preparation_abort_has_no_participant_effects() -> None:
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
    )
    second = participant(
        2,
        publication_intent=intent,
    )
    participants = participant_set(
        first,
        second,
    )
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        prepared_ids=(),
    )

    result = apply(
        store=Store(retained=retained),
        publication_id=intent.publication_id,
    )

    assert result == ()
    assert first.commit_calls == []
    assert first.abort_calls == []
    assert second.commit_calls == []
    assert second.abort_calls == []


def test_durable_record_is_read_before_any_effect() -> None:
    events: list[str] = []
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        events=events,
    )
    participants = participant_set(first)
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        prepared_ids=(first.participant_id,),
    )

    apply(
        store=Store(
            retained=retained,
            events=events,
        ),
        publication_id=intent.publication_id,
    )

    assert events == [
        "read",
        "commit:participant-001",
    ]


def test_application_never_prepares_or_creates() -> None:
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
    )
    participants = participant_set(first)
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        prepared_ids=(first.participant_id,),
    )
    store = Store(retained=retained)

    apply(
        store=store,
        publication_id=intent.publication_id,
    )

    assert first.prepare_calls == 0
    assert store.create_calls == 0


def test_ordinary_failure_does_not_block_later_participants() -> None:
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        commit_results=[
            RuntimeError("unavailable"),
        ],
    )
    second = participant(
        2,
        publication_intent=intent,
    )
    participants = participant_set(
        first,
        second,
    )
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        prepared_ids=(
            first.participant_id,
            second.participant_id,
        ),
    )

    with pytest.raises(ApplicationError) as captured:
        apply(
            store=Store(retained=retained),
            publication_id=intent.publication_id,
        )

    assert captured.value.failed_participant_ids == (
        "participant-001",
    )
    assert second.commit_calls == [
        intent.publication_id,
    ]


def test_multiple_failures_preserve_canonical_identifiers() -> None:
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        commit_results=[
            RuntimeError("first"),
        ],
    )
    second = participant(
        2,
        publication_intent=intent,
    )
    third = participant(
        3,
        publication_intent=intent,
        commit_results=[
            ValueError("third"),
        ],
    )
    participants = participant_set(
        first,
        second,
        third,
    )
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        prepared_ids=(
            first.participant_id,
            second.participant_id,
            third.participant_id,
        ),
    )

    with pytest.raises(ApplicationError) as captured:
        apply(
            store=Store(retained=retained),
            publication_id=intent.publication_id,
        )

    assert captured.value.failed_participant_ids == (
        "participant-001",
        "participant-003",
    )


@pytest.mark.parametrize(
    "invalid_result",
    (
        None,
        object(),
        "committed",
        True,
        1,
        (),
    ),
)
def test_non_state_confirmation_is_reported_as_failure(
    invalid_result: object,
) -> None:
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        commit_results=[
            invalid_result,
        ],
    )
    participants = participant_set(first)
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        prepared_ids=(first.participant_id,),
    )

    with pytest.raises(ApplicationError) as captured:
        apply(
            store=Store(retained=retained),
            publication_id=intent.publication_id,
        )

    assert captured.value.failed_participant_ids == (
        first.participant_id,
    )


def test_confirmation_for_other_intent_is_reported_as_failure() -> None:
    intent = create_intent(
        publication_id="publication-001",
        scalar=1,
    )
    other_intent = create_intent(
        publication_id="publication-001",
        scalar=2,
    )
    first = participant(
        1,
        publication_intent=intent,
        commit_results=[
            state(
                publication_intent=other_intent,
                phase=Phase.COMMITTED,
            ),
        ],
    )
    participants = participant_set(first)
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        prepared_ids=(first.participant_id,),
    )

    with pytest.raises(ApplicationError):
        apply(
            store=Store(retained=retained),
            publication_id=intent.publication_id,
        )


def test_confirmation_with_wrong_phase_is_reported_as_failure() -> None:
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        commit_results=[
            state(
                publication_intent=intent,
                phase=Phase.PREPARED,
            ),
        ],
    )
    participants = participant_set(first)
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        prepared_ids=(first.participant_id,),
    )

    with pytest.raises(ApplicationError):
        apply(
            store=Store(retained=retained),
            publication_id=intent.publication_id,
        )


def test_retry_reapplies_same_durable_decision() -> None:
    intent = create_intent()
    committed = state(
        publication_intent=intent,
        phase=Phase.COMMITTED,
    )
    first = participant(
        1,
        publication_intent=intent,
        commit_results=[
            RuntimeError("temporary"),
            committed,
        ],
    )
    second = participant(
        2,
        publication_intent=intent,
        commit_results=[
            committed,
            committed,
        ],
    )
    participants = participant_set(
        first,
        second,
    )
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        prepared_ids=(
            first.participant_id,
            second.participant_id,
        ),
    )
    store = Store(retained=retained)

    with pytest.raises(ApplicationError):
        apply(
            store=store,
            publication_id=intent.publication_id,
        )

    result = apply(
        store=store,
        publication_id=intent.publication_id,
    )

    assert result == (
        committed,
        committed,
    )
    assert first.commit_calls == [
        intent.publication_id,
        intent.publication_id,
    ]
    assert second.commit_calls == [
        intent.publication_id,
        intent.publication_id,
    ]
    assert store.read_calls == [
        intent.publication_id,
        intent.publication_id,
    ]


def test_keyboard_interrupt_is_not_converted_to_application_failure() -> None:
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        commit_results=[
            KeyboardInterrupt(),
        ],
    )
    participants = participant_set(first)
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        prepared_ids=(first.participant_id,),
    )

    with pytest.raises(KeyboardInterrupt):
        apply(
            store=Store(retained=retained),
            publication_id=intent.publication_id,
        )


def test_missing_durable_decision_is_rejected_without_effects() -> None:
    with pytest.raises(
        ValueError,
        match="does not exist",
    ):
        apply(
            store=Store(retained=None),
            publication_id="publication-001",
        )


@pytest.mark.parametrize(
    "value",
    (
        object(),
        "record",
        True,
        1,
        (),
    ),
)
def test_store_read_rejects_invalid_value(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="read",
    ):
        apply(
            store=Store(retained=value),
            publication_id="publication-001",
        )


def test_different_retained_publication_id_is_rejected() -> None:
    intent = create_intent(
        publication_id="publication-002",
    )
    first = participant(
        1,
        publication_intent=intent,
    )
    participants = participant_set(first)
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        prepared_ids=(first.participant_id,),
    )

    with pytest.raises(
        ValueError,
        match="different publication_id",
    ):
        apply(
            store=Store(retained=retained),
            publication_id="publication-001",
        )

    assert first.commit_calls == []


def test_preparation_outside_roster_is_rejected_before_effects() -> None:
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
    )
    participants = participant_set(first)
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        prepared_ids=("participant-999",),
    )

    with pytest.raises(
        ValueError,
        match="outside the participant set",
    ):
        apply(
            store=Store(retained=retained),
            publication_id=intent.publication_id,
        )

    assert first.commit_calls == []
    assert first.abort_calls == []


@pytest.mark.parametrize(
    ("prepared_ids", "changed_decision"),
    (
        ((), Decision.COMMIT),
        (("participant-001",), Decision.ABORT),
    ),
)
def test_contradictory_durable_decision_is_rejected_before_effects(
    prepared_ids: tuple[str, ...],
    changed_decision: Decision,
) -> None:
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
    )
    participants = participant_set(first)
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        prepared_ids=prepared_ids,
    )
    contradictory = replace(
        retained,
        decision=changed_decision,
    )

    with pytest.raises(
        ValueError,
        match="does not match",
    ):
        apply(
            store=Store(retained=contradictory),
            publication_id=intent.publication_id,
        )

    assert first.commit_calls == []
    assert first.abort_calls == []


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "store",
        True,
        1,
        (),
        IncompleteStore(),
    ),
)
def test_decision_record_store_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="decision_record_store",
    ):
        apply_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_recorded_decision(
            decision_record_store=value,
            publication_id="publication-001",
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        b"publication-001",
        True,
        1,
        (),
    ),
)
def test_publication_id_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="publication_id",
    ):
        apply_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_recorded_decision(
            decision_record_store=Store(
                retained=None,
            ),
            publication_id=value,
        )


def test_publication_id_rejects_empty_value() -> None:
    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        apply(
            store=Store(retained=None),
            publication_id="",
        )


def test_application_error_is_nominal_runtime_error() -> None:
    error = ApplicationError(
        failed_participant_ids=(
            "participant-001",
            "participant-003",
        ),
    )

    assert isinstance(error, RuntimeError)
    assert error.failed_participant_ids == (
        "participant-001",
        "participant-003",
    )


def test_application_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        apply_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_recorded_decision
    )

    assert tuple(signature.parameters) == (
        "decision_record_store",
        "publication_id",
    )
    assert all(
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )

    hints = get_type_hints(
        apply_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_recorded_decision
    )
    assert hints == {
        "decision_record_store": DecisionRecordStore,
        "publication_id": str,
        "return": tuple[PublicationState, ...],
    }


def test_application_defines_no_preparation_or_decision_creation() -> None:
    source = inspect.getsource(
        apply_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_recorded_decision
    )

    assert ".prepare(" not in source
    assert ".create(" not in source
    assert "collect_" not in source
    assert "sqlite" not in source.lower()
    assert "subprocess" not in source
    assert "socket" not in source
    assert "eval(" not in source
    assert "exec(" not in source
