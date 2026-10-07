import inspect
from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation,
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


Confirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation
)
Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
PublicationState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
)


def terminal_state(
    *,
    phase: Phase = Phase.COMMITTED,
    revision: int = 4,
    scalar: int = 1,
) -> PublicationState:
    return PublicationState(
        publication_intent=create_intent(
            scalar=scalar,
        ),
        phase=phase,
        revision=revision,
    )


def confirmation(
    *,
    participant_id: str = "participant-001",
    decision: Decision = Decision.COMMIT,
    publication_state: PublicationState | None = None,
) -> Confirmation:
    if publication_state is None:
        phase = (
            Phase.COMMITTED
            if decision is Decision.COMMIT
            else Phase.ABORTED
        )
        publication_state = terminal_state(
            phase=phase,
        )

    return Confirmation(
        participant_id=participant_id,
        decision=decision,
        publication_state=publication_state,
    )


def test_confirmation_has_exact_fields() -> None:
    assert tuple(
        field.name
        for field in fields(Confirmation)
    ) == (
        "participant_id",
        "decision",
        "publication_state",
    )


def test_confirmation_preserves_exact_values() -> None:
    publication_state = terminal_state()

    value = Confirmation(
        participant_id="participant-017",
        decision=Decision.COMMIT,
        publication_state=publication_state,
    )

    assert value.participant_id == "participant-017"
    assert value.decision is Decision.COMMIT
    assert value.publication_state is publication_state


def test_confirmation_is_frozen() -> None:
    value = confirmation()

    with pytest.raises(FrozenInstanceError):
        value.participant_id = "participant-002"


def test_confirmation_uses_slots() -> None:
    value = confirmation()

    assert not hasattr(value, "__dict__")
    assert Confirmation.__slots__ == (
        "participant_id",
        "decision",
        "publication_state",
    )


def test_equal_values_are_equal() -> None:
    publication_state = terminal_state()

    assert (
        confirmation(
            publication_state=publication_state,
        )
        == confirmation(
            publication_state=publication_state,
        )
    )


def test_different_participant_identifiers_are_not_equal() -> None:
    publication_state = terminal_state()

    assert (
        confirmation(
            participant_id="participant-001",
            publication_state=publication_state,
        )
        != confirmation(
            participant_id="participant-002",
            publication_state=publication_state,
        )
    )


def test_different_decisions_are_not_equal() -> None:
    assert (
        confirmation(
            decision=Decision.COMMIT,
        )
        != confirmation(
            decision=Decision.ABORT,
        )
    )


def test_different_terminal_states_are_not_equal() -> None:
    assert (
        confirmation(
            publication_state=terminal_state(
                revision=4,
            ),
        )
        != confirmation(
            publication_state=terminal_state(
                revision=5,
            ),
        )
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        True,
        1,
        b"participant-001",
        object(),
    ),
)
def test_participant_identifier_requires_exact_string(
    value,
) -> None:
    with pytest.raises(
        TypeError,
        match="participant_id must be a string",
    ):
        Confirmation(
            participant_id=value,
            decision=Decision.COMMIT,
            publication_state=terminal_state(),
        )


def test_empty_participant_identifier_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="participant_id must not be empty",
    ):
        Confirmation(
            participant_id="",
            decision=Decision.COMMIT,
            publication_state=terminal_state(),
        )


@pytest.mark.parametrize(
    "value",
    (
        " ",
        "\t",
        "participant/opaque",
        "PARTICIPANT-001",
    ),
)
def test_opaque_nonempty_participant_identifier_is_preserved(
    value: str,
) -> None:
    assert (
        confirmation(
            participant_id=value,
        ).participant_id
        == value
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        "COMMIT",
        "ABORT",
        True,
        1,
        object(),
    ),
)
def test_decision_requires_nominal_type(
    value,
) -> None:
    with pytest.raises(
        TypeError,
        match="decision must be a",
    ):
        Confirmation(
            participant_id="participant-001",
            decision=value,
            publication_state=terminal_state(),
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        True,
        1,
        "state",
        object(),
    ),
)
def test_publication_state_requires_nominal_type(
    value,
) -> None:
    with pytest.raises(
        TypeError,
        match="publication_state must be a",
    ):
        Confirmation(
            participant_id="participant-001",
            decision=Decision.COMMIT,
            publication_state=value,
        )


@pytest.mark.parametrize(
    ("decision", "phase"),
    (
        (
            Decision.COMMIT,
            Phase.COMMITTED,
        ),
        (
            Decision.ABORT,
            Phase.ABORTED,
        ),
    ),
)
def test_matching_terminal_phase_is_accepted(
    decision: Decision,
    phase: Phase,
) -> None:
    publication_state = terminal_state(
        phase=phase,
    )

    assert (
        confirmation(
            decision=decision,
            publication_state=publication_state,
        ).publication_state
        is publication_state
    )


@pytest.mark.parametrize(
    ("decision", "phase"),
    tuple(
        (
            decision,
            phase,
        )
        for decision in Decision
        for phase in Phase
        if (
            decision,
            phase,
        )
        not in (
            (
                Decision.COMMIT,
                Phase.COMMITTED,
            ),
            (
                Decision.ABORT,
                Phase.ABORTED,
            ),
        )
    ),
)
def test_nonmatching_phase_is_rejected(
    decision: Decision,
    phase: Phase,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "publication_state phase must confirm "
            "the retained publication decision"
        ),
    ):
        confirmation(
            decision=decision,
            publication_state=terminal_state(
                phase=phase,
            ),
        )


@pytest.mark.parametrize(
    "revision",
    (
        1,
        2,
        4,
        2**32,
        2**64 - 1,
    ),
)
def test_confirmation_preserves_any_valid_terminal_revision(
    revision: int,
) -> None:
    publication_state = terminal_state(
        revision=revision,
    )

    assert (
        confirmation(
            publication_state=publication_state,
        ).publication_state.revision
        == revision
    )


def test_confirmation_preserves_signed_publication_intent() -> None:
    publication_state = terminal_state(
        scalar=2,
    )

    value = confirmation(
        publication_state=publication_state,
    )

    assert (
        value.publication_state.publication_intent
        is publication_state.publication_intent
    )


def test_confirmation_defines_no_storage_behavior() -> None:
    source = inspect.getsource(Confirmation).lower()

    assert "sqlite" not in source
    assert "database" not in source
    assert "open(" not in source
    assert ".read(" not in source
    assert ".write(" not in source


def test_confirmation_defines_no_participant_effects() -> None:
    members = set(Confirmation.__dict__)

    assert "prepare" not in members
    assert "commit" not in members
    assert "abort" not in members


def test_confirmation_defines_validation_only() -> None:
    members = set(Confirmation.__dict__)

    assert members.isdisjoint(
        {
            "create",
            "read",
            "compare_and_swap",
            "coordinate",
            "apply",
            "retry",
        }
    )


def test_confirmation_imports_no_unsafe_capability() -> None:
    module = inspect.getmodule(Confirmation)
    assert module is not None

    source = inspect.getsource(module)

    assert "subprocess" not in source
    assert "socket" not in source
    assert "eval(" not in source
    assert "exec(" not in source
    assert "__import__" not in source
