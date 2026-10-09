import inspect
from typing import get_type_hints

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationApplicationCompletion,
)

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_coordinator import (
    coordinate_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication,
)
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
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation,
)

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet,
)

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationStore,
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
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    create_intent,
)


ApplicationCompletion = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationApplicationCompletion
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
PublicationIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent
)
Confirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation
)

ConfirmationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet
)

ConfirmationStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationStore
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
        prepare_results: list[object],
        commit_results: list[object],
        abort_results: list[object],
        events: list[str],
    ) -> None:
        self._participant_id = participant_id
        self.prepare_results = prepare_results
        self.commit_results = commit_results
        self.abort_results = abort_results
        self.events = events
        self.prepare_calls = 0
        self.commit_calls = 0
        self.abort_calls = 0

    @property
    def participant_id(self) -> str:
        return self._participant_id

    def prepare(
        self,
        *,
        publication_intent: PublicationIntent,
    ) -> PublicationState:
        self.prepare_calls += 1
        self.events.append(
            f"prepare:{self.participant_id}"
        )
        return self._next(self.prepare_results)

    def commit(
        self,
        *,
        publication_id: str,
    ) -> PublicationState:
        self.commit_calls += 1
        self.events.append(
            f"commit:{self.participant_id}"
        )
        return self._next(self.commit_results)

    def abort(
        self,
        *,
        publication_id: str,
    ) -> PublicationState:
        self.abort_calls += 1
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
        events: list[str],
        retained: object = None,
        create_result: object = True,
    ) -> None:
        self.events = events
        self.retained = retained
        self.create_result = create_result
        self.read_calls = 0
        self.create_calls = 0

    def read(
        self,
        *,
        publication_id: str,
    ) -> DecisionRecord | None:
        self.read_calls += 1
        retained_decision = getattr(
            self.retained,
            "decision",
            None,
        )
        retained_label = (
            retained_decision.value
            if retained_decision is not None
            else "NONE"
        )
        self.events.append(
            f"read:{retained_label}"
        )
        return self.retained

    def create(
        self,
        *,
        decision_record: DecisionRecord,
    ) -> bool:
        self.create_calls += 1
        self.events.append(
            f"create:{decision_record.decision.value}"
        )

        if self.create_result is True:
            self.retained = decision_record

        return self.create_result


class ConfirmationStoreDouble:
    def __init__(self) -> None:
        self.retained = ConfirmationSet(
            confirmations=(),
        )
        self.read_calls: list[str] = []
        self.create_calls: list[Confirmation] = []

    def read(
        self,
        *,
        publication_id: str,
    ) -> ConfirmationSet:
        self.read_calls.append(publication_id)
        return self.retained

    def create(
        self,
        *,
        confirmation: Confirmation,
    ) -> bool:
        self.create_calls.append(confirmation)
        retained = {
            item.participant_id: item
            for item in self.retained.confirmations
        }
        retained[confirmation.participant_id] = (
            confirmation
        )
        self.retained = ConfirmationSet(
            confirmations=tuple(
                retained[participant_id]
                for participant_id in sorted(retained)
            ),
        )
        return True


class IncompleteConfirmationStore:
    pass


class IncompleteStore:
    pass


def state(
    *,
    publication_intent: PublicationIntent,
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
    publication_intent: PublicationIntent,
    events: list[str],
    prepare_results: list[object] | None = None,
    commit_results: list[object] | None = None,
    abort_results: list[object] | None = None,
) -> Participant:
    if prepare_results is None:
        prepare_results = [
            state(
                publication_intent=publication_intent,
                phase=Phase.PREPARED,
            )
        ]
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
        prepare_results=prepare_results,
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


def retained_decision(
    *,
    publication_intent: PublicationIntent,
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


def coordinate(
    *,
    publication_intent: PublicationIntent,
    participants: ParticipantSet,
    store: DecisionRecordStore,
    confirmation_store: ConfirmationStore | None = None,
) -> ApplicationCompletion:
    if confirmation_store is None:
        confirmation_store = ConfirmationStoreDouble()

    return (
        coordinate_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication(
            publication_intent=publication_intent,
            participant_set=participants,
            decision_record_store=store,
            confirmation_store=confirmation_store,
        )
    )


def test_commit_is_persisted_before_any_commit_effect() -> None:
    events: list[str] = []
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        events=events,
    )
    second = participant(
        2,
        publication_intent=intent,
        events=events,
    )
    participants = participant_set(
        first,
        second,
    )
    store = Store(events=events)

    result = coordinate(
        publication_intent=intent,
        participants=participants,
        store=store,
    )

    assert result.decision_record.decision is Decision.COMMIT
    assert store.retained is result.decision_record
    assert events == [
        "read:NONE",
        "prepare:participant-001",
        "prepare:participant-002",
        "create:COMMIT",
        "read:COMMIT",
        "commit:participant-001",
        "commit:participant-002",
        "read:COMMIT",
    ]


def test_abort_is_persisted_before_prepared_participant_abort() -> None:
    events: list[str] = []
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        events=events,
    )
    second = participant(
        2,
        publication_intent=intent,
        events=events,
        prepare_results=[
            RuntimeError("unavailable"),
        ],
    )
    participants = participant_set(
        first,
        second,
    )
    store = Store(events=events)

    result = coordinate(
        publication_intent=intent,
        participants=participants,
        store=store,
    )

    assert result.decision_record.decision is Decision.ABORT
    assert events == [
        "read:NONE",
        "prepare:participant-001",
        "prepare:participant-002",
        "create:ABORT",
        "read:ABORT",
        "abort:participant-001",
        "read:ABORT",
    ]
    assert second.abort_calls == 0


def test_zero_preparation_abort_requires_no_final_effect() -> None:
    events: list[str] = []
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        events=events,
        prepare_results=[
            RuntimeError("unavailable"),
        ],
    )
    second = participant(
        2,
        publication_intent=intent,
        events=events,
        prepare_results=[
            RuntimeError("unavailable"),
        ],
    )
    participants = participant_set(
        first,
        second,
    )
    store = Store(events=events)

    result = coordinate(
        publication_intent=intent,
        participants=participants,
        store=store,
    )

    assert result.decision_record.decision is Decision.ABORT
    assert events == [
        "read:NONE",
        "prepare:participant-001",
        "prepare:participant-002",
        "create:ABORT",
        "read:ABORT",
        "read:ABORT",
    ]
    assert first.abort_calls == 0
    assert second.abort_calls == 0


def test_existing_decision_skips_preparation_and_creation() -> None:
    events: list[str] = []
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        events=events,
    )
    participants = participant_set(first)
    retained = retained_decision(
        publication_intent=intent,
        participants=participants,
        prepared_ids=(first.participant_id,),
    )
    store = Store(
        events=events,
        retained=retained,
    )

    result = coordinate(
        publication_intent=intent,
        participants=participants,
        store=store,
    )

    assert result.decision_record is retained
    assert first.prepare_calls == 0
    assert store.create_calls == 0
    assert events == [
        "read:COMMIT",
        "read:COMMIT",
        "commit:participant-001",
        "read:COMMIT",
    ]


def test_partial_application_preserves_durable_decision() -> None:
    events: list[str] = []
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        events=events,
        commit_results=[
            RuntimeError("temporary"),
        ],
    )
    participants = participant_set(first)
    store = Store(events=events)

    with pytest.raises(ApplicationError) as captured:
        coordinate(
            publication_intent=intent,
            participants=participants,
            store=store,
        )

    assert captured.value.failed_participant_ids == (
        first.participant_id,
    )
    assert store.retained is not None
    assert store.retained.decision is Decision.COMMIT
    assert events.index("create:COMMIT") < events.index(
        "commit:participant-001"
    )


def test_retry_uses_durable_decision_without_repreparing() -> None:
    events: list[str] = []
    intent = create_intent()
    committed = state(
        publication_intent=intent,
        phase=Phase.COMMITTED,
    )
    first = participant(
        1,
        publication_intent=intent,
        events=events,
        commit_results=[
            RuntimeError("temporary"),
            committed,
        ],
    )
    second = participant(
        2,
        publication_intent=intent,
        events=events,
        commit_results=[
            committed,
        ],
    )
    participants = participant_set(
        first,
        second,
    )
    store = Store(events=events)
    confirmation_store = ConfirmationStoreDouble()

    with pytest.raises(ApplicationError):
        coordinate(
            publication_intent=intent,
            participants=participants,
            store=store,
            confirmation_store=confirmation_store,
        )

    result = coordinate(
        publication_intent=intent,
        participants=participants,
        store=store,
        confirmation_store=confirmation_store,
    )

    assert result.decision_record is store.retained
    assert result.decision_record.decision is Decision.COMMIT
    assert first.prepare_calls == 1
    assert second.prepare_calls == 1
    assert first.commit_calls == 2
    assert second.commit_calls == 1
    assert store.create_calls == 1
    assert confirmation_store.read_calls == [
        intent.publication_id,
        intent.publication_id,
        intent.publication_id,
    ]
    assert tuple(
        confirmation.participant_id
        for confirmation in confirmation_store.create_calls
    ) == (
        second.participant_id,
        first.participant_id,
    )


def test_create_failure_prevents_every_final_effect() -> None:
    events: list[str] = []
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        events=events,
    )
    participants = participant_set(first)
    store = Store(
        events=events,
        create_result=None,
    )

    with pytest.raises(
        TypeError,
        match="create must return a bool",
    ):
        coordinate(
            publication_intent=intent,
            participants=participants,
            store=store,
        )

    assert first.commit_calls == 0
    assert first.abort_calls == 0
    assert store.retained is None
    assert all(
        not event.startswith("commit:")
        and not event.startswith("abort:")
        for event in events
    )


def test_existing_abort_is_reapplied_without_preparation() -> None:
    events: list[str] = []
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        events=events,
    )
    second = participant(
        2,
        publication_intent=intent,
        events=events,
    )
    participants = participant_set(
        first,
        second,
    )
    retained = retained_decision(
        publication_intent=intent,
        participants=participants,
        prepared_ids=(first.participant_id,),
    )
    store = Store(
        events=events,
        retained=retained,
    )

    result = coordinate(
        publication_intent=intent,
        participants=participants,
        store=store,
    )

    assert result.decision_record is retained
    assert result.decision_record.decision is Decision.ABORT
    assert first.prepare_calls == 0
    assert second.prepare_calls == 0
    assert first.abort_calls == 1
    assert second.abort_calls == 0


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "intent",
        True,
        1,
        (),
    ),
)
def test_invalid_publication_intent_fails_before_effects(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="publication_intent",
    ):
        coordinate_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication(
            publication_intent=value,
            participant_set=object(),
            decision_record_store=object(),
            confirmation_store=ConfirmationStoreDouble(),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "participants",
        True,
        1,
        (),
    ),
)
def test_invalid_participant_set_fails_before_effects(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="participant_set",
    ):
        coordinate_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication(
            publication_intent=create_intent(),
            participant_set=value,
            decision_record_store=object(),
            confirmation_store=ConfirmationStoreDouble(),
        )


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
def test_invalid_store_fails_before_effects(
    value: object,
) -> None:
    events: list[str] = []
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        events=events,
    )
    participants = participant_set(first)

    with pytest.raises(
        TypeError,
        match="decision_record_store",
    ):
        coordinate_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication(
            publication_intent=intent,
            participant_set=participants,
            decision_record_store=value,
            confirmation_store=ConfirmationStoreDouble(),
        )

    assert events == []


def test_coordinator_returns_exact_durable_completion() -> None:
    events: list[str] = []
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        events=events,
    )
    participants = participant_set(first)
    store = Store(
        events=events,
    )
    confirmation_store = ConfirmationStoreDouble()

    result = coordinate(
        publication_intent=intent,
        participants=participants,
        store=store,
        confirmation_store=confirmation_store,
    )

    assert isinstance(
        result,
        ApplicationCompletion,
    )
    assert result.decision_record is store.retained
    assert (
        result.confirmation_set
        is confirmation_store.retained
    )
    assert tuple(
        confirmation.participant_id
        for confirmation in (
            result.confirmation_set.confirmations
        )
    ) == (
        first.participant_id,
    )


def test_missing_completion_after_successful_application_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: list[str] = []
    intent = create_intent()
    first = participant(
        1,
        publication_intent=intent,
        events=events,
    )
    participants = participant_set(first)
    store = Store(
        events=events,
    )
    confirmation_store = ConfirmationStoreDouble()

    monkeypatch.setattr(
        (
            "sp001.services."
            "security_admission_evidence_coverage_closure_state_"
            "merkle_checkpoint_publication_coordinator."
            "read_security_admission_evidence_coverage_closure_"
            "state_merkle_checkpoint_publication_application_completion"
        ),
        lambda **kwargs: None,
    )

    with pytest.raises(
        RuntimeError,
        match="must produce exhaustive durable completion",
    ):
        coordinate(
            publication_intent=intent,
            participants=participants,
            store=store,
            confirmation_store=confirmation_store,
        )

    assert store.retained is not None
    assert confirmation_store.retained.confirmations


def test_coordinator_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        coordinate_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication
    )

    assert tuple(signature.parameters) == (
        "publication_intent",
        "participant_set",
        "decision_record_store",
        "confirmation_store",
    )
    assert all(
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )

    hints = get_type_hints(
        coordinate_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication
    )
    assert hints == {
        "publication_intent": PublicationIntent,
        "participant_set": ParticipantSet,
        "decision_record_store": DecisionRecordStore,
        "confirmation_store": ConfirmationStore,
        "return": ApplicationCompletion,
    }


def test_coordinator_delegates_without_transport_or_retry_policy() -> None:
    source = inspect.getsource(
        coordinate_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication
    )

    assert source.count("record_security_admission") == 1
    assert source.count("apply_security_admission") == 1
    assert source.count("read_security_admission") == 1
    assert ".prepare(" not in source
    assert ".commit(" not in source
    assert ".abort(" not in source
    assert ".create(" not in source
    assert ".read(" not in source
    assert "while " not in source
    assert "sleep" not in source
    assert "timeout" not in source
    assert "subprocess" not in source
    assert "socket" not in source
