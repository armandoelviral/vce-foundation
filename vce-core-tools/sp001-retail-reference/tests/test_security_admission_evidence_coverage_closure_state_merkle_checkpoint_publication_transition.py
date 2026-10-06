import inspect
from itertools import product

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_transition import (
    transition_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    create_state,
)


Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
transition = (
    transition_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication
)

UINT64_MAX = (1 << 64) - 1

ALLOWED_TRANSITIONS = frozenset(
    {
        (
            Phase.INTENT_RECORDED,
            Phase.PREPARED,
        ),
        (
            Phase.INTENT_RECORDED,
            Phase.ABORT_DECIDED,
        ),
        (
            Phase.PREPARED,
            Phase.COMMIT_DECIDED,
        ),
        (
            Phase.PREPARED,
            Phase.ABORT_DECIDED,
        ),
        (
            Phase.COMMIT_DECIDED,
            Phase.COMMITTED,
        ),
        (
            Phase.ABORT_DECIDED,
            Phase.ABORTED,
        ),
    }
)

ALL_TRANSITIONS = tuple(product(tuple(Phase), repeat=2))

REJECTED_TRANSITIONS = tuple(
    candidate
    for candidate in ALL_TRANSITIONS
    if candidate not in ALLOWED_TRANSITIONS
)


def test_transition_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(transition)

    assert tuple(signature.parameters) == (
        "current_state",
        "target_phase",
    )
    assert all(
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )


@pytest.mark.parametrize(
    "source_phase,target_phase",
    tuple(ALLOWED_TRANSITIONS),
)
def test_every_allowed_transition_succeeds(
    source_phase: Phase,
    target_phase: Phase,
) -> None:
    current_state = create_state(
        phase=source_phase,
        revision=7,
    )

    next_state = transition(
        current_state=current_state,
        target_phase=target_phase,
    )

    assert next_state.publication_intent is (
        current_state.publication_intent
    )
    assert next_state.phase is target_phase
    assert next_state.revision == 8


@pytest.mark.parametrize(
    "source_phase,target_phase",
    REJECTED_TRANSITIONS,
)
def test_every_unlisted_transition_fails_closed(
    source_phase: Phase,
    target_phase: Phase,
) -> None:
    current_state = create_state(
        phase=source_phase,
        revision=7,
    )

    with pytest.raises(
        ValueError,
        match="publication phase transition is not allowed",
    ):
        transition(
            current_state=current_state,
            target_phase=target_phase,
        )


@pytest.mark.parametrize("phase", tuple(Phase))
def test_same_phase_transition_is_rejected(
    phase: Phase,
) -> None:
    current_state = create_state(
        phase=phase,
        revision=11,
    )

    with pytest.raises(ValueError):
        transition(
            current_state=current_state,
            target_phase=phase,
        )


def test_commit_decision_can_only_reach_committed() -> None:
    current_state = create_state(
        phase=Phase.COMMIT_DECIDED,
        revision=3,
    )

    next_state = transition(
        current_state=current_state,
        target_phase=Phase.COMMITTED,
    )

    assert next_state.phase is Phase.COMMITTED
    assert next_state.revision == 4


@pytest.mark.parametrize(
    "forbidden_target",
    (
        Phase.INTENT_RECORDED,
        Phase.PREPARED,
        Phase.COMMIT_DECIDED,
        Phase.ABORT_DECIDED,
        Phase.ABORTED,
    ),
)
def test_commit_decision_never_allows_abort_or_regression(
    forbidden_target: Phase,
) -> None:
    current_state = create_state(
        phase=Phase.COMMIT_DECIDED,
        revision=3,
    )

    with pytest.raises(ValueError):
        transition(
            current_state=current_state,
            target_phase=forbidden_target,
        )


def test_abort_decision_can_only_reach_aborted() -> None:
    current_state = create_state(
        phase=Phase.ABORT_DECIDED,
        revision=3,
    )

    next_state = transition(
        current_state=current_state,
        target_phase=Phase.ABORTED,
    )

    assert next_state.phase is Phase.ABORTED
    assert next_state.revision == 4


@pytest.mark.parametrize(
    "terminal_phase",
    (
        Phase.COMMITTED,
        Phase.ABORTED,
    ),
)
@pytest.mark.parametrize("target_phase", tuple(Phase))
def test_terminal_phases_have_no_outgoing_transition(
    terminal_phase: Phase,
    target_phase: Phase,
) -> None:
    current_state = create_state(
        phase=terminal_phase,
        revision=5,
    )

    with pytest.raises(ValueError):
        transition(
            current_state=current_state,
            target_phase=target_phase,
        )


@pytest.mark.parametrize(
    "source_phase,target_phase",
    tuple(ALLOWED_TRANSITIONS),
)
def test_transition_does_not_mutate_current_state(
    source_phase: Phase,
    target_phase: Phase,
) -> None:
    current_state = create_state(
        phase=source_phase,
        revision=13,
    )
    intent = current_state.publication_intent

    transition(
        current_state=current_state,
        target_phase=target_phase,
    )

    assert current_state.publication_intent is intent
    assert current_state.phase is source_phase
    assert current_state.revision == 13


@pytest.mark.parametrize(
    "revision",
    (
        1,
        2,
        7,
        65537,
        UINT64_MAX - 1,
    ),
)
def test_transition_increments_revision_exactly_once(
    revision: int,
) -> None:
    current_state = create_state(
        phase=Phase.INTENT_RECORDED,
        revision=revision,
    )

    next_state = transition(
        current_state=current_state,
        target_phase=Phase.PREPARED,
    )

    assert next_state.revision == revision + 1


def test_transition_rejects_revision_overflow() -> None:
    current_state = create_state(
        phase=Phase.INTENT_RECORDED,
        revision=UINT64_MAX,
    )

    with pytest.raises(
        ValueError,
        match="publication revision cannot exceed uint64",
    ):
        transition(
            current_state=current_state,
            target_phase=Phase.PREPARED,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "state",
        1,
        (),
    ),
)
def test_current_state_rejects_invalid_nominal_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "current_state must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationState"
        ),
    ):
        transition(
            current_state=value,
            target_phase=Phase.PREPARED,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "PREPARED",
        1,
        (),
    ),
)
def test_target_phase_rejects_invalid_nominal_type(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "target_phase must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationPhase"
        ),
    ):
        transition(
            current_state=create_state(),
            target_phase=value,
        )


def test_illegal_transition_does_not_consume_revision() -> None:
    current_state = create_state(
        phase=Phase.PREPARED,
        revision=19,
    )

    with pytest.raises(ValueError):
        transition(
            current_state=current_state,
            target_phase=Phase.INTENT_RECORDED,
        )

    assert current_state.phase is Phase.PREPARED
    assert current_state.revision == 19


def test_transition_defines_no_external_capability() -> None:
    source = inspect.getsource(transition)

    for forbidden_term in (
        "open(",
        "sqlite",
        "socket",
        "subprocess",
        "commit(",
        "rollback(",
        "sleep(",
    ):
        assert forbidden_term not in source.lower()
