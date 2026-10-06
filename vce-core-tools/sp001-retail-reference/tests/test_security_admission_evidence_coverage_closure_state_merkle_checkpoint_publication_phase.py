import inspect
from enum import StrEnum

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)


Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)


def test_phase_is_str_enum() -> None:
    assert issubclass(Phase, StrEnum)


def test_phase_has_exact_members() -> None:
    assert tuple(Phase) == (
        Phase.INTENT_RECORDED,
        Phase.PREPARED,
        Phase.COMMIT_DECIDED,
        Phase.COMMITTED,
        Phase.ABORT_DECIDED,
        Phase.ABORTED,
    )


def test_phase_has_exact_names() -> None:
    assert tuple(
        member.name
        for member in Phase
    ) == (
        "INTENT_RECORDED",
        "PREPARED",
        "COMMIT_DECIDED",
        "COMMITTED",
        "ABORT_DECIDED",
        "ABORTED",
    )


def test_phase_has_exact_values() -> None:
    assert tuple(
        member.value
        for member in Phase
    ) == (
        "INTENT_RECORDED",
        "PREPARED",
        "COMMIT_DECIDED",
        "COMMITTED",
        "ABORT_DECIDED",
        "ABORTED",
    )


@pytest.mark.parametrize(
    "phase",
    tuple(Phase),
)
def test_phase_is_string_compatible(
    phase: Phase,
) -> None:
    assert isinstance(phase, str)
    assert str(phase) == phase.value


@pytest.mark.parametrize(
    "phase",
    tuple(Phase),
)
def test_phase_round_trips_from_value(
    phase: Phase,
) -> None:
    assert Phase(phase.value) is phase


@pytest.mark.parametrize(
    "value",
    (
        "",
        "UNKNOWN",
        "PREPARE",
        "COMMIT",
        "ABORT",
        "ROLLED_BACK",
        "FAILED",
        "RETRYING",
        "intent_recorded",
        "committed",
    ),
)
def test_unknown_phase_is_rejected(
    value: str,
) -> None:
    with pytest.raises(ValueError):
        Phase(value)


def test_phase_has_no_aliases() -> None:
    assert len(Phase.__members__) == len(
        tuple(Phase)
    )


def test_commit_decision_and_completion_are_distinct() -> None:
    assert (
        Phase.COMMIT_DECIDED
        is not Phase.COMMITTED
    )
    assert (
        Phase.COMMIT_DECIDED.value
        != Phase.COMMITTED.value
    )


def test_abort_decision_and_completion_are_distinct() -> None:
    assert (
        Phase.ABORT_DECIDED
        is not Phase.ABORTED
    )
    assert (
        Phase.ABORT_DECIDED.value
        != Phase.ABORTED.value
    )


def test_phase_defines_no_transition_behavior() -> None:
    source = inspect.getsource(Phase).lower()
    forbidden = (
        "def transition",
        "def prepare",
        "def commit",
        "def abort",
        "rollback",
        "database",
        "network",
    )

    assert all(
        token not in source
        for token in forbidden
    )


def test_phase_does_not_authorize_admission() -> None:
    source = inspect.getsource(Phase).lower()
    forbidden = (
        "admission_decision",
        "authorization",
        "authority",
        "rejection",
        "classification",
    )

    assert all(
        token not in source
        for token in forbidden
    )
