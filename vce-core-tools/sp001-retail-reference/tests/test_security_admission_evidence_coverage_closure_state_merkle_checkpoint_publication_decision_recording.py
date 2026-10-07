import inspect
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
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_recording import (
    record_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
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
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    create_intent,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_collection import (
    Participant,
    participant,
    participant_set,
    publication_state,
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
ParticipantPreparation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation
)
ParticipantPreparationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet
)
ParticipantSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet
)


class Store:
    def __init__(
        self,
        *,
        retained: object = None,
        create_result: object = True,
        conflict_record: object = None,
    ) -> None:
        self.retained = retained
        self.create_result = create_result
        self.conflict_record = conflict_record
        self.read_calls: list[str] = []
        self.create_calls: list[DecisionRecord] = []

    def read(
        self,
        *,
        publication_id: str,
    ) -> DecisionRecord | None:
        self.read_calls.append(publication_id)
        return self.retained

    def create(
        self,
        *,
        decision_record: DecisionRecord,
    ) -> bool:
        self.create_calls.append(decision_record)

        if self.create_result is True:
            self.retained = decision_record
        elif self.create_result is False:
            self.retained = self.conflict_record

        return self.create_result


class IncompleteStore:
    pass


def prepared_participants(
    *,
    publication_intent: PublicationIntent,
    size: int = 3,
) -> ParticipantSet:
    return participant_set(
        *(
            participant(
                index,
                prepare_result=publication_state(
                    publication_intent=publication_intent,
                ),
            )
            for index in range(1, size + 1)
        )
    )


def decision_record(
    *,
    publication_intent: PublicationIntent,
    participants: ParticipantSet,
    decision: Decision,
) -> DecisionRecord:
    if decision is Decision.COMMIT:
        preparations = tuple(
            ParticipantPreparation(
                participant_id=value.participant_id,
                publication_state=publication_state(
                    publication_intent=publication_intent,
                ),
            )
            for value in participants.participants
        )
    else:
        preparations = ()

    return (
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision(
            publication_intent=publication_intent,
            participant_set=participants,
            preparation_set=ParticipantPreparationSet(
                preparations=preparations,
            ),
        )
    )


def record(
    *,
    publication_intent: PublicationIntent,
    participants: ParticipantSet,
    store: DecisionRecordStore,
) -> DecisionRecord:
    return (
        record_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision(
            publication_intent=publication_intent,
            participant_set=participants,
            decision_record_store=store,
        )
    )


def test_exhaustive_preparations_are_durably_recorded_as_commit() -> None:
    intent = create_intent()
    participants = prepared_participants(
        publication_intent=intent,
    )
    store = Store()

    result = record(
        publication_intent=intent,
        participants=participants,
        store=store,
    )

    assert result.decision is Decision.COMMIT
    assert store.retained is result
    assert store.create_calls == [result]
    assert tuple(
        preparation.participant_id
        for preparation in result.preparation_set.preparations
    ) == (
        "participant-001",
        "participant-002",
        "participant-003",
    )


def test_missing_preparation_is_durably_recorded_as_abort() -> None:
    intent = create_intent()
    first = participant(
        1,
        prepare_result=publication_state(
            publication_intent=intent,
        ),
    )
    second = participant(
        2,
        prepare_result=object(),
        prepare_error=RuntimeError("unavailable"),
    )
    participants = participant_set(
        first,
        second,
    )
    store = Store()

    result = record(
        publication_intent=intent,
        participants=participants,
        store=store,
    )

    assert result.decision is Decision.ABORT
    assert tuple(
        preparation.participant_id
        for preparation in result.preparation_set.preparations
    ) == ("participant-001",)
    assert store.retained is result


def test_zero_preparations_are_durably_recorded_as_abort() -> None:
    intent = create_intent()
    participants = participant_set(
        participant(
            1,
            prepare_result=object(),
            prepare_error=RuntimeError("unavailable"),
        ),
        participant(
            2,
            prepare_result=object(),
            prepare_error=RuntimeError("unavailable"),
        ),
    )
    store = Store()

    result = record(
        publication_intent=intent,
        participants=participants,
        store=store,
    )

    assert result.decision is Decision.ABORT
    assert result.preparation_set.preparations == ()
    assert store.retained is result


def test_existing_durable_decision_is_returned_exactly() -> None:
    intent = create_intent()
    participants = prepared_participants(
        publication_intent=intent,
    )
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        decision=Decision.COMMIT,
    )
    store = Store(
        retained=retained,
    )

    result = record(
        publication_intent=intent,
        participants=participants,
        store=store,
    )

    assert result is retained
    assert store.create_calls == []
    assert store.read_calls == [
        intent.publication_id,
    ]


def test_existing_decision_prevents_repreparation() -> None:
    intent = create_intent()
    participant_value = participant(
        1,
        prepare_result=publication_state(
            publication_intent=intent,
        ),
    )
    participants = participant_set(
        participant_value,
    )
    retained = decision_record(
        publication_intent=intent,
        participants=participants,
        decision=Decision.COMMIT,
    )

    record(
        publication_intent=intent,
        participants=participants,
        store=Store(
            retained=retained,
        ),
    )

    assert participant_value.prepare_calls == []


def test_successful_create_reads_store_only_before_preparation() -> None:
    intent = create_intent()
    participants = prepared_participants(
        publication_intent=intent,
    )
    store = Store()

    result = record(
        publication_intent=intent,
        participants=participants,
        store=store,
    )

    assert store.read_calls == [
        intent.publication_id,
    ]
    assert store.create_calls == [result]


def test_create_conflict_adopts_exact_durable_winner() -> None:
    intent = create_intent()
    participants = prepared_participants(
        publication_intent=intent,
    )
    winner = decision_record(
        publication_intent=intent,
        participants=participants,
        decision=Decision.ABORT,
    )
    store = Store(
        create_result=False,
        conflict_record=winner,
    )

    result = record(
        publication_intent=intent,
        participants=participants,
        store=store,
    )

    assert result is winner
    assert len(store.create_calls) == 1
    assert store.create_calls[0].decision is Decision.COMMIT
    assert store.read_calls == [
        intent.publication_id,
        intent.publication_id,
    ]


def test_create_conflict_without_retained_decision_fails_closed() -> None:
    intent = create_intent()
    participants = prepared_participants(
        publication_intent=intent,
    )

    with pytest.raises(
        RuntimeError,
        match="did not retain",
    ):
        record(
            publication_intent=intent,
            participants=participants,
            store=Store(
                create_result=False,
                conflict_record=None,
            ),
        )


def test_existing_other_intent_is_rejected_before_preparation() -> None:
    intent = create_intent(
        publication_id="publication-001",
        scalar=1,
    )
    other_intent = create_intent(
        publication_id="publication-001",
        scalar=2,
    )
    participants = prepared_participants(
        publication_intent=intent,
    )
    retained = decision_record(
        publication_intent=other_intent,
        participants=participants,
        decision=Decision.ABORT,
    )

    with pytest.raises(
        ValueError,
        match="different publication intent",
    ):
        record(
            publication_intent=intent,
            participants=participants,
            store=Store(
                retained=retained,
            ),
        )

    assert all(
        value.prepare_calls == []
        for value in participants.participants
    )


def test_existing_other_participant_set_is_rejected() -> None:
    intent = create_intent()
    participants = prepared_participants(
        publication_intent=intent,
        size=2,
    )
    other_participants = participant_set(
        participant(
            9,
            prepare_result=publication_state(
                publication_intent=intent,
            ),
        ),
    )
    retained = decision_record(
        publication_intent=intent,
        participants=other_participants,
        decision=Decision.ABORT,
    )

    with pytest.raises(
        ValueError,
        match="different participant set",
    ):
        record(
            publication_intent=intent,
            participants=participants,
            store=Store(
                retained=retained,
            ),
        )


def test_conflict_winner_with_other_intent_is_rejected() -> None:
    intent = create_intent(
        publication_id="publication-001",
        scalar=1,
    )
    other_intent = create_intent(
        publication_id="publication-001",
        scalar=2,
    )
    participants = prepared_participants(
        publication_intent=intent,
    )
    winner = decision_record(
        publication_intent=other_intent,
        participants=participants,
        decision=Decision.ABORT,
    )

    with pytest.raises(
        ValueError,
        match="different publication intent",
    ):
        record(
            publication_intent=intent,
            participants=participants,
            store=Store(
                create_result=False,
                conflict_record=winner,
            ),
        )


def test_conflict_winner_with_other_participant_set_is_rejected() -> None:
    intent = create_intent()
    participants = prepared_participants(
        publication_intent=intent,
        size=2,
    )
    other_participants = participant_set(
        participant(
            9,
            prepare_result=publication_state(
                publication_intent=intent,
            ),
        ),
    )
    winner = decision_record(
        publication_intent=intent,
        participants=other_participants,
        decision=Decision.ABORT,
    )

    with pytest.raises(
        ValueError,
        match="different participant set",
    ):
        record(
            publication_intent=intent,
            participants=participants,
            store=Store(
                create_result=False,
                conflict_record=winner,
            ),
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
def test_initial_read_rejects_invalid_value(
    value: object,
) -> None:
    intent = create_intent()
    participants = prepared_participants(
        publication_intent=intent,
    )

    with pytest.raises(
        TypeError,
        match="read",
    ):
        record(
            publication_intent=intent,
            participants=participants,
            store=Store(
                retained=value,
            ),
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
def test_conflict_read_rejects_invalid_value(
    value: object,
) -> None:
    intent = create_intent()
    participants = prepared_participants(
        publication_intent=intent,
    )

    with pytest.raises(
        TypeError,
        match="read after create conflict",
    ):
        record(
            publication_intent=intent,
            participants=participants,
            store=Store(
                create_result=False,
                conflict_record=value,
            ),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "created",
        0,
        1,
        (),
    ),
)
def test_create_requires_nominal_bool(
    value: object,
) -> None:
    intent = create_intent()
    participants = prepared_participants(
        publication_intent=intent,
    )

    with pytest.raises(
        TypeError,
        match="create must return a bool",
    ):
        record(
            publication_intent=intent,
            participants=participants,
            store=Store(
                create_result=value,
            ),
        )


def test_no_participant_decision_effect_occurs() -> None:
    intent = create_intent()
    participants = prepared_participants(
        publication_intent=intent,
    )

    record(
        publication_intent=intent,
        participants=participants,
        store=Store(),
    )

    assert all(
        value.commit_calls == []
        for value in participants.participants
    )
    assert all(
        value.abort_calls == []
        for value in participants.participants
    )


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
def test_publication_intent_rejects_invalid_type(
    value: object,
) -> None:
    intent = create_intent()
    participants = prepared_participants(
        publication_intent=intent,
    )

    with pytest.raises(
        TypeError,
        match="publication_intent",
    ):
        record_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision(
            publication_intent=value,
            participant_set=participants,
            decision_record_store=Store(),
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
def test_participant_set_rejects_invalid_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="participant_set",
    ):
        record_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision(
            publication_intent=create_intent(),
            participant_set=value,
            decision_record_store=Store(),
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
def test_decision_record_store_rejects_invalid_type(
    value: object,
) -> None:
    intent = create_intent()
    participants = prepared_participants(
        publication_intent=intent,
    )

    with pytest.raises(
        TypeError,
        match="decision_record_store",
    ):
        record_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision(
            publication_intent=intent,
            participant_set=participants,
            decision_record_store=value,
        )


def test_recording_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        record_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision
    )

    assert tuple(signature.parameters) == (
        "publication_intent",
        "participant_set",
        "decision_record_store",
    )
    assert all(
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )

    hints = get_type_hints(
        record_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision
    )
    assert hints == {
        "publication_intent": PublicationIntent,
        "participant_set": ParticipantSet,
        "decision_record_store": DecisionRecordStore,
        "return": DecisionRecord,
    }


def test_recording_defines_no_participant_decision_effects() -> None:
    source = inspect.getsource(
        record_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision
    )

    assert ".commit(" not in source
    assert ".abort(" not in source
    assert "sqlite" not in source.lower()
    assert "subprocess" not in source
    assert "socket" not in source
    assert "eval(" not in source
    assert "exec(" not in source
