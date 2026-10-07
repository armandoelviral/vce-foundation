import inspect
from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    confirmation,
    terminal_state,
)


ConfirmationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet
)
Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)


def create_set(
    *,
    size: int = 3,
    decision: Decision = Decision.COMMIT,
    scalar: int = 1,
) -> ConfirmationSet:
    phase = (
        Phase.COMMITTED
        if decision is Decision.COMMIT
        else Phase.ABORTED
    )
    publication_state = terminal_state(
        phase=phase,
        scalar=scalar,
    )

    return ConfirmationSet(
        confirmations=tuple(
            confirmation(
                participant_id=f"participant-{index:03d}",
                decision=decision,
                publication_state=publication_state,
            )
            for index in range(1, size + 1)
        ),
    )


def test_confirmation_set_has_exact_field() -> None:
    assert tuple(
        field.name
        for field in fields(ConfirmationSet)
    ) == (
        "confirmations",
    )


def test_confirmation_set_preserves_exact_tuple() -> None:
    confirmations = create_set().confirmations

    value = ConfirmationSet(
        confirmations=confirmations,
    )

    assert value.confirmations is confirmations


def test_confirmation_set_is_frozen() -> None:
    value = create_set()

    with pytest.raises(FrozenInstanceError):
        value.confirmations = ()


def test_confirmation_set_uses_slots() -> None:
    value = create_set()

    assert not hasattr(value, "__dict__")
    assert ConfirmationSet.__slots__ == (
        "confirmations",
    )


def test_equal_values_are_equal() -> None:
    confirmations = create_set().confirmations

    assert (
        ConfirmationSet(
            confirmations=confirmations,
        )
        == ConfirmationSet(
            confirmations=confirmations,
        )
    )


def test_different_confirmation_tuples_are_not_equal() -> None:
    assert create_set(size=2) != create_set(size=3)


def test_empty_set_is_preserved() -> None:
    value = ConfirmationSet(
        confirmations=(),
    )

    assert value.confirmations == ()


@pytest.mark.parametrize(
    "value",
    (
        None,
        [],
        {},
        set(),
        "confirmations",
        object(),
    ),
)
def test_confirmations_require_tuple(
    value,
) -> None:
    with pytest.raises(
        TypeError,
        match="confirmations must be a tuple",
    ):
        ConfirmationSet(
            confirmations=value,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        True,
        1,
        "confirmation",
        object(),
    ),
)
def test_members_require_nominal_confirmation_type(
    value,
) -> None:
    with pytest.raises(
        TypeError,
        match="must contain only",
    ):
        ConfirmationSet(
            confirmations=(
                value,
            ),
        )


@pytest.mark.parametrize(
    "size",
    (
        1,
        2,
        3,
        8,
    ),
)
def test_canonical_confirmation_cardinality_is_preserved(
    size: int,
) -> None:
    value = create_set(
        size=size,
    )

    assert len(value.confirmations) == size


def test_duplicate_participant_identifier_is_rejected() -> None:
    retained = create_set(
        size=1,
    ).confirmations[0]

    with pytest.raises(
        ValueError,
        match="unique participant identifiers",
    ):
        ConfirmationSet(
            confirmations=(
                retained,
                retained,
            ),
        )


def test_duplicate_identifier_is_rejected_for_distinct_states() -> None:
    first = confirmation(
        participant_id="participant-001",
        publication_state=terminal_state(
            revision=4,
        ),
    )
    second = confirmation(
        participant_id="participant-001",
        publication_state=terminal_state(
            revision=5,
        ),
    )

    with pytest.raises(
        ValueError,
        match="unique participant identifiers",
    ):
        ConfirmationSet(
            confirmations=(
                first,
                second,
            ),
        )


def test_noncanonical_participant_order_is_rejected() -> None:
    confirmations = create_set().confirmations

    with pytest.raises(
        ValueError,
        match="canonical participant identifier order",
    ):
        ConfirmationSet(
            confirmations=tuple(
                reversed(confirmations)
            ),
        )


def test_lexical_identifier_order_is_canonical() -> None:
    publication_state = terminal_state()

    value = ConfirmationSet(
        confirmations=(
            confirmation(
                participant_id="participant-02",
                publication_state=publication_state,
            ),
            confirmation(
                participant_id="participant-1",
                publication_state=publication_state,
            ),
            confirmation(
                participant_id="participant-10",
                publication_state=publication_state,
            ),
        ),
    )

    assert tuple(
        item.participant_id
        for item in value.confirmations
    ) == (
        "participant-02",
        "participant-1",
        "participant-10",
    )


def test_commit_confirmations_are_preserved() -> None:
    value = create_set(
        decision=Decision.COMMIT,
    )

    assert all(
        item.decision is Decision.COMMIT
        for item in value.confirmations
    )
    assert all(
        item.publication_state.phase is Phase.COMMITTED
        for item in value.confirmations
    )


def test_abort_confirmations_are_preserved() -> None:
    value = create_set(
        decision=Decision.ABORT,
    )

    assert all(
        item.decision is Decision.ABORT
        for item in value.confirmations
    )
    assert all(
        item.publication_state.phase is Phase.ABORTED
        for item in value.confirmations
    )


def test_mixed_decisions_are_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="same publication decision",
    ):
        ConfirmationSet(
            confirmations=(
                confirmation(
                    participant_id="participant-001",
                    decision=Decision.COMMIT,
                ),
                confirmation(
                    participant_id="participant-002",
                    decision=Decision.ABORT,
                ),
            ),
        )


def test_same_signed_publication_intent_is_preserved() -> None:
    value = create_set(
        size=3,
        scalar=2,
    )
    retained_intent = (
        value.confirmations[0]
        .publication_state
        .publication_intent
    )

    assert all(
        (
            item
            .publication_state
            .publication_intent
        )
        is retained_intent
        for item in value.confirmations
    )


def test_equal_but_distinct_intent_values_are_accepted() -> None:
    first_state = terminal_state(
        scalar=1,
    )
    copied_intent = replace(
        first_state.publication_intent,
    )
    second_state = type(first_state)(
        publication_intent=copied_intent,
        phase=first_state.phase,
        revision=first_state.revision,
    )

    assert (
        first_state.publication_intent
        == second_state.publication_intent
    )
    assert (
        first_state.publication_intent
        is not second_state.publication_intent
    )

    value = ConfirmationSet(
        confirmations=(
            confirmation(
                participant_id="participant-001",
                publication_state=first_state,
            ),
            confirmation(
                participant_id="participant-002",
                publication_state=second_state,
            ),
        ),
    )

    assert len(value.confirmations) == 2


def test_different_signed_publication_intents_are_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="exact same publication intent",
    ):
        ConfirmationSet(
            confirmations=(
                confirmation(
                    participant_id="participant-001",
                    publication_state=terminal_state(
                        scalar=1,
                    ),
                ),
                confirmation(
                    participant_id="participant-002",
                    publication_state=terminal_state(
                        scalar=2,
                    ),
                ),
            ),
        )


def test_different_terminal_revisions_are_allowed() -> None:
    first_state = terminal_state(
        revision=4,
    )
    second_state = type(first_state)(
        publication_intent=(
            first_state.publication_intent
        ),
        phase=first_state.phase,
        revision=7,
    )

    value = ConfirmationSet(
        confirmations=(
            confirmation(
                participant_id="participant-001",
                publication_state=first_state,
            ),
            confirmation(
                participant_id="participant-002",
                publication_state=second_state,
            ),
        ),
    )

    assert tuple(
        item.publication_state.revision
        for item in value.confirmations
    ) == (
        4,
        7,
    )


def test_set_does_not_claim_exhaustive_participant_coverage() -> None:
    value = create_set(
        size=1,
    )

    assert len(value.confirmations) == 1
    assert not hasattr(value, "participant_set")
    assert not hasattr(value, "exhaustive")


def test_set_defines_no_storage_behavior() -> None:
    source = inspect.getsource(ConfirmationSet).lower()

    assert "sqlite" not in source
    assert "database" not in source
    assert "open(" not in source
    assert ".read(" not in source
    assert ".write(" not in source


def test_set_defines_no_participant_effects() -> None:
    members = set(ConfirmationSet.__dict__)

    assert members.isdisjoint(
        {
            "prepare",
            "commit",
            "abort",
            "apply",
            "coordinate",
        }
    )


def test_set_defines_validation_only() -> None:
    members = set(ConfirmationSet.__dict__)

    assert members.isdisjoint(
        {
            "create",
            "read",
            "compare_and_swap",
            "retry",
            "verify",
        }
    )


def test_set_imports_no_unsafe_capability() -> None:
    module = inspect.getmodule(ConfirmationSet)
    assert module is not None

    source = inspect.getsource(module)

    assert "subprocess" not in source
    assert "socket" not in source
    assert "eval(" not in source
    assert "exec(" not in source
    assert "__import__" not in source
