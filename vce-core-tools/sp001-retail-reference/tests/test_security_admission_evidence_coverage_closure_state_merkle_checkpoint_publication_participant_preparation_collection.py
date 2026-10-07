import inspect
from dataclasses import FrozenInstanceError
from typing import get_type_hints

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_collection import (
    collect_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparations,
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
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    create_intent,
)


PublicationIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent
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


class Participant:
    def __init__(
        self,
        *,
        participant_id: str,
        prepare_result: object,
        prepare_error: BaseException | None = None,
    ) -> None:
        self._participant_id = participant_id
        self._prepare_result = prepare_result
        self._prepare_error = prepare_error
        self.prepare_calls: list[PublicationIntent] = []
        self.commit_calls: list[str] = []
        self.abort_calls: list[str] = []

    @property
    def participant_id(self) -> str:
        return self._participant_id

    def prepare(
        self,
        *,
        publication_intent: PublicationIntent,
    ) -> PublicationState:
        self.prepare_calls.append(
            publication_intent
        )

        if self._prepare_error is not None:
            raise self._prepare_error

        return self._prepare_result

    def commit(
        self,
        *,
        publication_id: str,
    ) -> PublicationState:
        self.commit_calls.append(publication_id)
        raise AssertionError(
            "collection must not commit participants"
        )

    def abort(
        self,
        *,
        publication_id: str,
    ) -> PublicationState:
        self.abort_calls.append(publication_id)
        raise AssertionError(
            "collection must not abort participants"
        )


def publication_state(
    *,
    publication_intent: PublicationIntent,
    phase: Phase = Phase.PREPARED,
) -> PublicationState:
    return PublicationState(
        publication_intent=publication_intent,
        phase=phase,
        revision=2,
    )


def participant(
    index: int,
    *,
    prepare_result: object,
    prepare_error: BaseException | None = None,
) -> Participant:
    return Participant(
        participant_id=f"participant-{index:03d}",
        prepare_result=prepare_result,
        prepare_error=prepare_error,
    )


def participant_set(
    *participants: Participant,
) -> ParticipantSet:
    return ParticipantSet(
        participants=participants,
    )


def collect(
    *,
    publication_intent: PublicationIntent,
    participants: ParticipantSet,
) -> ParticipantPreparationSet:
    return (
        collect_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparations(
            publication_intent=publication_intent,
            participant_set=participants,
        )
    )


def test_exact_prepared_evidence_is_collected_in_canonical_order() -> None:
    intent = create_intent()
    first_state = publication_state(
        publication_intent=intent,
    )
    second_state = publication_state(
        publication_intent=intent,
    )
    first = participant(
        1,
        prepare_result=first_state,
    )
    second = participant(
        2,
        prepare_result=second_state,
    )

    result = collect(
        publication_intent=intent,
        participants=participant_set(
            first,
            second,
        ),
    )

    assert tuple(
        preparation.participant_id
        for preparation in result.preparations
    ) == (
        "participant-001",
        "participant-002",
    )
    assert (
        result.preparations[0].publication_state
        is first_state
    )
    assert (
        result.preparations[1].publication_state
        is second_state
    )


def test_result_is_nominal_preparation_set() -> None:
    intent = create_intent()

    result = collect(
        publication_intent=intent,
        participants=participant_set(
            participant(
                1,
                prepare_result=publication_state(
                    publication_intent=intent,
                ),
            ),
        ),
    )

    assert type(result) is ParticipantPreparationSet


def test_all_ordinary_failures_produce_empty_evidence() -> None:
    intent = create_intent()

    result = collect(
        publication_intent=intent,
        participants=participant_set(
            participant(
                1,
                prepare_result=object(),
                prepare_error=RuntimeError("unavailable"),
            ),
            participant(
                2,
                prepare_result=object(),
                prepare_error=ValueError("rejected"),
            ),
        ),
    )

    assert result.preparations == ()


def test_partial_failure_retains_only_conclusive_evidence() -> None:
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
    third_state = publication_state(
        publication_intent=intent,
    )
    third = participant(
        3,
        prepare_result=third_state,
    )

    result = collect(
        publication_intent=intent,
        participants=participant_set(
            first,
            second,
            third,
        ),
    )

    assert tuple(
        preparation.participant_id
        for preparation in result.preparations
    ) == (
        "participant-001",
        "participant-003",
    )
    assert (
        result.preparations[1].publication_state
        is third_state
    )


def test_collection_continues_after_ordinary_failure() -> None:
    intent = create_intent()
    later = participant(
        2,
        prepare_result=publication_state(
            publication_intent=intent,
        ),
    )

    collect(
        publication_intent=intent,
        participants=participant_set(
            participant(
                1,
                prepare_result=object(),
                prepare_error=RuntimeError("unavailable"),
            ),
            later,
        ),
    )

    assert later.prepare_calls == [intent]


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "prepared",
        True,
        1,
        (),
    ),
)
def test_non_state_response_is_omitted(
    value: object,
) -> None:
    intent = create_intent()

    result = collect(
        publication_intent=intent,
        participants=participant_set(
            participant(
                1,
                prepare_result=value,
            ),
        ),
    )

    assert result.preparations == ()


def test_state_for_other_signed_intent_is_omitted() -> None:
    intent = create_intent(
        publication_id="publication-001",
        scalar=1,
    )
    other_intent = create_intent(
        publication_id="publication-002",
        scalar=2,
    )

    result = collect(
        publication_intent=intent,
        participants=participant_set(
            participant(
                1,
                prepare_result=publication_state(
                    publication_intent=other_intent,
                ),
            ),
        ),
    )

    assert result.preparations == ()


@pytest.mark.parametrize(
    "phase",
    tuple(
        phase
        for phase in Phase
        if phase is not Phase.PREPARED
    ),
)
def test_non_prepared_phase_is_omitted(
    phase: Phase,
) -> None:
    intent = create_intent()

    result = collect(
        publication_intent=intent,
        participants=participant_set(
            participant(
                1,
                prepare_result=publication_state(
                    publication_intent=intent,
                    phase=phase,
                ),
            ),
        ),
    )

    assert result.preparations == ()


def test_each_participant_receives_exact_intent_once() -> None:
    intent = create_intent()
    first = participant(
        1,
        prepare_result=publication_state(
            publication_intent=intent,
        ),
    )
    second = participant(
        2,
        prepare_result=publication_state(
            publication_intent=intent,
        ),
    )

    collect(
        publication_intent=intent,
        participants=participant_set(
            first,
            second,
        ),
    )

    assert first.prepare_calls == [intent]
    assert second.prepare_calls == [intent]


def test_collection_never_commits_or_aborts() -> None:
    intent = create_intent()
    retained = participant(
        1,
        prepare_result=publication_state(
            publication_intent=intent,
        ),
    )

    collect(
        publication_intent=intent,
        participants=participant_set(
            retained,
        ),
    )

    assert retained.commit_calls == []
    assert retained.abort_calls == []


def test_keyboard_interrupt_is_not_converted_to_missing_evidence() -> None:
    intent = create_intent()

    with pytest.raises(KeyboardInterrupt):
        collect(
            publication_intent=intent,
            participants=participant_set(
                participant(
                    1,
                    prepare_result=object(),
                    prepare_error=KeyboardInterrupt(),
                ),
            ),
        )


def test_system_exit_is_not_converted_to_missing_evidence() -> None:
    intent = create_intent()

    with pytest.raises(SystemExit):
        collect(
            publication_intent=intent,
            participants=participant_set(
                participant(
                    1,
                    prepare_result=object(),
                    prepare_error=SystemExit(1),
                ),
            ),
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

    with pytest.raises(
        TypeError,
        match="publication_intent",
    ):
        collect_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparations(
            publication_intent=value,
            participant_set=participant_set(
                participant(
                    1,
                    prepare_result=publication_state(
                        publication_intent=intent,
                    ),
                ),
            ),
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
        collect_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparations(
            publication_intent=create_intent(),
            participant_set=value,
        )


def test_collection_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(
        collect_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparations
    )

    assert tuple(signature.parameters) == (
        "publication_intent",
        "participant_set",
    )
    assert all(
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )

    hints = get_type_hints(
        collect_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparations
    )
    assert hints == {
        "publication_intent": PublicationIntent,
        "participant_set": ParticipantSet,
        "return": ParticipantPreparationSet,
    }


def test_returned_set_is_immutable() -> None:
    intent = create_intent()
    result = collect(
        publication_intent=intent,
        participants=participant_set(
            participant(
                1,
                prepare_result=publication_state(
                    publication_intent=intent,
                ),
            ),
        ),
    )

    with pytest.raises(FrozenInstanceError):
        result.preparations = ()


def test_collection_defines_no_decision_or_persistence_effects() -> None:
    source = inspect.getsource(
        collect_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparations
    )

    assert "derive_" not in source
    assert "decision_record" not in source
    assert "sqlite" not in source.lower()
    assert ".create(" not in source
    assert ".read(" not in source
    assert ".commit(" not in source
    assert ".abort(" not in source


def test_collection_imports_no_unsafe_dynamic_capability() -> None:
    module = inspect.getmodule(
        collect_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparations
    )
    assert module is not None

    source = inspect.getsource(module)

    assert "subprocess" not in source
    assert "socket" not in source
    assert "eval(" not in source
    assert "exec(" not in source
    assert "pickle" not in source
