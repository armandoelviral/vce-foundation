import inspect

from dataclasses import replace
from typing import get_type_hints

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationApplicationCompletion,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion_derivation import (
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion import (
    abort_record,
    commit_record,
    confirmation_set,
    zero_preparation_abort,
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
Confirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation
)
ConfirmationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet
)
Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
derive = (
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion
)


def test_derivation_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(derive)

    assert tuple(signature.parameters) == (
        "decision_record",
        "confirmation_set",
    )
    assert all(
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )

    hints = get_type_hints(derive)
    assert hints == {
        "decision_record": DecisionRecord,
        "confirmation_set": ConfirmationSet,
        "return": ApplicationCompletion | None,
    }


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        3,
        7,
    ),
)
def test_exact_commit_coverage_derives_completion(
    size: int,
) -> None:
    decision_record = commit_record(
        size=size,
    )
    confirmations = confirmation_set(
        decision_record,
    )

    result = derive(
        decision_record=decision_record,
        confirmation_set=confirmations,
    )

    assert isinstance(
        result,
        ApplicationCompletion,
    )
    assert result.decision_record is decision_record
    assert result.confirmation_set is confirmations


def test_exact_incomplete_abort_target_derives_completion() -> None:
    decision_record = abort_record()
    confirmations = confirmation_set(
        decision_record,
    )

    result = derive(
        decision_record=decision_record,
        confirmation_set=confirmations,
    )

    assert result == ApplicationCompletion(
        decision_record=decision_record,
        confirmation_set=confirmations,
    )


def test_zero_preparation_abort_derives_empty_completion() -> None:
    decision_record = zero_preparation_abort()
    confirmations = ConfirmationSet(
        confirmations=(),
    )

    result = derive(
        decision_record=decision_record,
        confirmation_set=confirmations,
    )

    assert result == ApplicationCompletion(
        decision_record=decision_record,
        confirmation_set=confirmations,
    )


def test_missing_commit_confirmation_is_not_complete() -> None:
    decision_record = commit_record()
    exhaustive = confirmation_set(
        decision_record,
    )
    incomplete = ConfirmationSet(
        confirmations=(
            exhaustive.confirmations[:-1]
        ),
    )

    assert (
        derive(
            decision_record=decision_record,
            confirmation_set=incomplete,
        )
        is None
    )


def test_empty_commit_confirmations_are_not_complete() -> None:
    assert (
        derive(
            decision_record=commit_record(),
            confirmation_set=ConfirmationSet(
                confirmations=(),
            ),
        )
        is None
    )


def test_missing_abort_confirmation_is_not_complete() -> None:
    decision_record = abort_record()
    exhaustive = confirmation_set(
        decision_record,
    )
    assert exhaustive.confirmations

    incomplete = ConfirmationSet(
        confirmations=(
            exhaustive.confirmations[:-1]
        ),
    )

    assert (
        derive(
            decision_record=decision_record,
            confirmation_set=incomplete,
        )
        is None
    )


def test_completion_is_deterministic() -> None:
    decision_record = commit_record()
    confirmations = confirmation_set(
        decision_record,
    )

    first = derive(
        decision_record=decision_record,
        confirmation_set=confirmations,
    )
    second = derive(
        decision_record=decision_record,
        confirmation_set=confirmations,
    )

    assert first == second


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
        derive(
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
        derive(
            decision_record=commit_record(),
            confirmation_set=value,
        )


def test_confirmation_outside_commit_target_fails_closed() -> None:
    decision_record = commit_record()
    exhaustive = confirmation_set(
        decision_record,
    )
    retained = exhaustive.confirmations[-1]

    outside = Confirmation(
        participant_id="participant-999",
        decision=retained.decision,
        publication_state=retained.publication_state,
    )
    changed = ConfirmationSet(
        confirmations=(
            *exhaustive.confirmations,
            outside,
        ),
    )

    with pytest.raises(
        ValueError,
        match="outside the application target",
    ):
        derive(
            decision_record=decision_record,
            confirmation_set=changed,
        )


def test_same_cardinality_with_different_roster_fails_closed() -> None:
    decision_record = commit_record()
    exhaustive = confirmation_set(
        decision_record,
    )
    retained = exhaustive.confirmations[0]

    changed_first = replace(
        retained,
        participant_id="participant-000",
    )
    changed = ConfirmationSet(
        confirmations=(
            changed_first,
            *exhaustive.confirmations[1:],
        ),
    )

    with pytest.raises(
        ValueError,
        match="outside the application target",
    ):
        derive(
            decision_record=decision_record,
            confirmation_set=changed,
        )


def test_contradictory_decision_record_fails_closed() -> None:
    retained = commit_record()
    contradictory = replace(
        retained,
        decision=Decision.ABORT,
    )
    confirmations = confirmation_set(
        retained,
    )

    with pytest.raises(
        ValueError,
        match="exactly re-derived publication decision",
    ):
        derive(
            decision_record=contradictory,
            confirmation_set=confirmations,
        )


def test_contradictory_decision_with_incomplete_confirmations_fails_closed() -> None:
    retained = commit_record()
    contradictory = replace(
        retained,
        decision=Decision.ABORT,
    )

    with pytest.raises(
        ValueError,
        match="exactly re-derived publication decision",
    ):
        derive(
            decision_record=contradictory,
            confirmation_set=ConfirmationSet(
                confirmations=(),
            ),
        )


def test_different_confirmation_decision_fails_closed() -> None:
    decision_record = commit_record()
    exhaustive = confirmation_set(
        decision_record,
    )

    changed = ConfirmationSet(
        confirmations=tuple(
            Confirmation(
                participant_id=confirmation.participant_id,
                decision=Decision.ABORT,
                publication_state=replace(
                    confirmation.publication_state,
                    phase=Phase.ABORTED,
                ),
            )
            for confirmation in exhaustive.confirmations
        ),
    )

    with pytest.raises(
        ValueError,
        match="recorded publication decision",
    ):
        derive(
            decision_record=decision_record,
            confirmation_set=changed,
        )


def test_different_signed_intent_fails_closed() -> None:
    decision_record = commit_record()
    exhaustive = confirmation_set(
        decision_record,
    )
    different_intent = create_intent(
        publication_id="different-publication",
    )

    changed = ConfirmationSet(
        confirmations=tuple(
            replace(
                confirmation,
                publication_state=replace(
                    confirmation.publication_state,
                    publication_intent=different_intent,
                ),
            )
            for confirmation in exhaustive.confirmations
        ),
    )

    with pytest.raises(
        ValueError,
        match="exact recorded publication intent",
    ):
        derive(
            decision_record=decision_record,
            confirmation_set=changed,
        )


def test_derivation_defines_no_effect_or_persistence() -> None:
    source = inspect.getsource(derive)

    assert ".prepare(" not in source
    assert ".commit(" not in source
    assert ".abort(" not in source
    assert ".create(" not in source
    assert ".read(" not in source
    assert "sqlite" not in source.lower()
    assert "open(" not in source
    assert "subprocess" not in source
    assert "socket" not in source
