import inspect

from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationApplicationCompletion,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_derivation import (
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_deserialization import (
    project_abort_with_incomplete_preparations,
    project_commit,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    create_intent,
)


Completion = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationApplicationCompletion
)
Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
Confirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation
)
ConfirmationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet
)
PreparationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet
)
Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)


def confirmation_set(
    decision_record,
) -> ConfirmationSet:
    preparation_by_id = {
        preparation.participant_id: preparation
        for preparation in (
            decision_record.preparation_set.preparations
        )
    }

    target_ids = (
        tuple(
            participant.participant_id
            for participant in (
                decision_record.participant_set.participants
            )
        )
        if decision_record.decision is Decision.COMMIT
        else tuple(preparation_by_id)
    )
    phase = (
        Phase.COMMITTED
        if decision_record.decision is Decision.COMMIT
        else Phase.ABORTED
    )

    return ConfirmationSet(
        confirmations=tuple(
            Confirmation(
                participant_id=participant_id,
                decision=decision_record.decision,
                publication_state=replace(
                    preparation_by_id[
                        participant_id
                    ].publication_state,
                    phase=phase,
                    revision=(
                        preparation_by_id[
                            participant_id
                        ].publication_state.revision
                        + 1
                    ),
                ),
            )
            for participant_id in target_ids
        ),
    )


def commit_record(
    *,
    size: int = 3,
):
    return project_commit(size=size)[0]


def abort_record():
    return project_abort_with_incomplete_preparations()[0]


def zero_preparation_abort():
    retained = commit_record()
    return (
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision(
            publication_intent=retained.publication_intent,
            participant_set=retained.participant_set,
            preparation_set=PreparationSet(
                preparations=(),
            ),
        )
    )


def completion(
    decision_record=None,
) -> Completion:
    if decision_record is None:
        decision_record = commit_record()

    return Completion(
        decision_record=decision_record,
        confirmation_set=confirmation_set(
            decision_record
        ),
    )


def test_completion_has_exact_fields() -> None:
    assert tuple(
        Completion.__dataclass_fields__
    ) == (
        "decision_record",
        "confirmation_set",
    )


def test_commit_completion_preserves_exact_graph() -> None:
    decision_record = commit_record()

    value = completion(decision_record)

    assert value.decision_record is decision_record
    assert (
        value.confirmation_set
        == confirmation_set(decision_record)
    )


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        3,
        7,
    ),
)
def test_every_exhaustive_commit_roster_completes(
    size: int,
) -> None:
    decision_record = commit_record(size=size)

    value = completion(decision_record)

    assert tuple(
        confirmation.participant_id
        for confirmation in (
            value.confirmation_set.confirmations
        )
    ) == tuple(
        participant.participant_id
        for participant in (
            decision_record.participant_set.participants
        )
    )


def test_incomplete_abort_target_completes() -> None:
    decision_record = abort_record()

    value = completion(decision_record)

    assert tuple(
        confirmation.participant_id
        for confirmation in (
            value.confirmation_set.confirmations
        )
    ) == tuple(
        preparation.participant_id
        for preparation in (
            decision_record.preparation_set.preparations
        )
    )


def test_zero_preparation_abort_completes_without_confirmations() -> None:
    decision_record = zero_preparation_abort()

    value = completion(decision_record)

    assert decision_record.decision is Decision.ABORT
    assert value.confirmation_set.confirmations == ()


def test_completion_is_frozen() -> None:
    value = completion()

    with pytest.raises(FrozenInstanceError):
        value.decision_record = abort_record()


def test_completion_uses_slots() -> None:
    value = completion()

    with pytest.raises(AttributeError):
        value.unexpected = object()


def test_equal_evidence_graphs_are_equal() -> None:
    decision_record = commit_record()

    assert (
        completion(decision_record)
        == completion(decision_record)
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "decision",
        1,
        True,
    ),
)
def test_decision_record_requires_nominal_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="decision_record",
    ):
        Completion(
            decision_record=value,
            confirmation_set=ConfirmationSet(
                confirmations=(),
            ),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        (),
        1,
        True,
    ),
)
def test_confirmation_set_requires_nominal_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="confirmation_set",
    ):
        Completion(
            decision_record=commit_record(),
            confirmation_set=value,
        )


def test_contradictory_decision_record_is_rejected() -> None:
    decision_record = commit_record()
    contradictory = replace(
        decision_record,
        decision=Decision.ABORT,
    )

    with pytest.raises(
        ValueError,
        match="re-derived",
    ):
        Completion(
            decision_record=contradictory,
            confirmation_set=ConfirmationSet(
                confirmations=(),
            ),
        )


def test_missing_commit_confirmation_is_rejected() -> None:
    decision_record = commit_record()
    confirmations = confirmation_set(
        decision_record
    )

    with pytest.raises(
        ValueError,
        match="exhaustively",
    ):
        Completion(
            decision_record=decision_record,
            confirmation_set=ConfirmationSet(
                confirmations=(
                    confirmations.confirmations[:-1]
                ),
            ),
        )


def test_missing_abort_confirmation_is_rejected() -> None:
    decision_record = abort_record()

    with pytest.raises(
        ValueError,
        match="exhaustively",
    ):
        Completion(
            decision_record=decision_record,
            confirmation_set=ConfirmationSet(
                confirmations=(),
            ),
        )


def test_confirmation_for_different_decision_is_rejected() -> None:
    decision_record = commit_record(size=1)
    retained = confirmation_set(
        decision_record
    ).confirmations[0]
    changed = Confirmation(
        participant_id=retained.participant_id,
        decision=Decision.ABORT,
        publication_state=replace(
            retained.publication_state,
            phase=Phase.ABORTED,
        ),
    )

    with pytest.raises(
        ValueError,
        match="recorded publication decision",
    ):
        Completion(
            decision_record=decision_record,
            confirmation_set=ConfirmationSet(
                confirmations=(changed,),
            ),
        )


def test_confirmation_for_different_signed_intent_is_rejected() -> None:
    decision_record = commit_record(size=1)
    retained = confirmation_set(
        decision_record
    ).confirmations[0]
    different_intent = create_intent(
        publication_id="different-publication",
    )
    changed = Confirmation(
        participant_id=retained.participant_id,
        decision=retained.decision,
        publication_state=replace(
            retained.publication_state,
            publication_intent=different_intent,
        ),
    )

    with pytest.raises(
        ValueError,
        match="recorded publication intent",
    ):
        Completion(
            decision_record=decision_record,
            confirmation_set=ConfirmationSet(
                confirmations=(changed,),
            ),
        )


def test_completion_defines_validation_only() -> None:
    members = set(Completion.__dict__)

    assert members.isdisjoint(
        {
            "prepare",
            "commit",
            "abort",
            "apply",
            "coordinate",
            "create",
            "read",
            "compare_and_swap",
            "retry",
        }
    )


def test_completion_imports_no_unsafe_capability() -> None:
    module = inspect.getmodule(Completion)
    assert module is not None

    source = inspect.getsource(module)

    assert "sqlite" not in source.lower()
    assert "subprocess" not in source
    assert "socket" not in source
    assert "open(" not in source
    assert "eval(" not in source
    assert "exec(" not in source
