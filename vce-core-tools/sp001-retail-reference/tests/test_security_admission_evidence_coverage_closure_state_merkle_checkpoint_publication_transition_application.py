import inspect
from dataclasses import dataclass, field
from itertools import product

import pytest

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_transition_application import (
    apply_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_transition,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    create_state,
)


Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
apply_transition = (
    apply_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_transition
)

UINT64_MAX = (1 << 64) - 1

ALLOWED_TRANSITIONS = (
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
)

REJECTED_TRANSITIONS = tuple(
    candidate
    for candidate in product(tuple(Phase), repeat=2)
    if candidate not in ALLOWED_TRANSITIONS
)


@dataclass
class RecordingStateStore:
    state: object
    swap_result: object = True
    read_failure: Exception | None = None
    swap_failure: Exception | None = None
    events: list[tuple[object, ...]] = field(
        default_factory=list
    )

    def read(
        self,
        *,
        publication_id: str,
    ):
        self.events.append(
            (
                "read",
                publication_id,
            )
        )
        if self.read_failure is not None:
            raise self.read_failure
        return self.state

    def create(
        self,
        *,
        state,
    ) -> bool:
        self.events.append(
            (
                "create",
                state,
            )
        )
        return True

    def compare_and_swap(
        self,
        *,
        expected_revision: int,
        next_state,
    ):
        self.events.append(
            (
                "compare_and_swap",
                expected_revision,
                next_state,
            )
        )
        if self.swap_failure is not None:
            raise self.swap_failure
        return self.swap_result


def test_application_has_exact_keyword_only_api() -> None:
    signature = inspect.signature(apply_transition)

    assert tuple(signature.parameters) == (
        "state_store",
        "publication_id",
        "expected_revision",
        "target_phase",
    )
    assert all(
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )


@pytest.mark.parametrize(
    "source_phase,target_phase",
    ALLOWED_TRANSITIONS,
)
def test_every_legal_transition_is_applied_once(
    source_phase: Phase,
    target_phase: Phase,
) -> None:
    current_state = create_state(
        publication_id="publication-001",
        phase=source_phase,
        revision=7,
    )
    store = RecordingStateStore(
        state=current_state,
    )

    next_state = apply_transition(
        state_store=store,
        publication_id="publication-001",
        expected_revision=7,
        target_phase=target_phase,
    )

    assert next_state.publication_intent is (
        current_state.publication_intent
    )
    assert next_state.phase is target_phase
    assert next_state.revision == 8
    assert store.events == [
        (
            "read",
            "publication-001",
        ),
        (
            "compare_and_swap",
            7,
            next_state,
        ),
    ]


@pytest.mark.parametrize(
    "source_phase,target_phase",
    REJECTED_TRANSITIONS,
)
def test_illegal_transition_fails_before_cas(
    source_phase: Phase,
    target_phase: Phase,
) -> None:
    current_state = create_state(
        phase=source_phase,
        revision=7,
    )
    store = RecordingStateStore(
        state=current_state,
    )

    with pytest.raises(
        ValueError,
        match="publication phase transition is not allowed",
    ):
        apply_transition(
            state_store=store,
            publication_id="publication-001",
            expected_revision=7,
            target_phase=target_phase,
        )

    assert store.events == [
        (
            "read",
            "publication-001",
        )
    ]


def test_missing_state_fails_closed_without_cas() -> None:
    store = RecordingStateStore(state=None)

    with pytest.raises(
        ValueError,
        match="publication state does not exist",
    ):
        apply_transition(
            state_store=store,
            publication_id="publication-001",
            expected_revision=1,
            target_phase=Phase.PREPARED,
        )

    assert store.events == [
        (
            "read",
            "publication-001",
        )
    ]


def test_stale_revision_fails_before_cas() -> None:
    store = RecordingStateStore(
        state=create_state(revision=2),
    )

    with pytest.raises(
        ValueError,
        match=(
            "publication revision conflict before "
            "compare-and-swap"
        ),
    ):
        apply_transition(
            state_store=store,
            publication_id="publication-001",
            expected_revision=1,
            target_phase=Phase.PREPARED,
        )

    assert store.events == [
        (
            "read",
            "publication-001",
        )
    ]


def test_race_lost_during_cas_fails_closed() -> None:
    current_state = create_state(revision=1)
    store = RecordingStateStore(
        state=current_state,
        swap_result=False,
    )

    with pytest.raises(
        ValueError,
        match=(
            "publication revision conflict during "
            "compare-and-swap"
        ),
    ):
        apply_transition(
            state_store=store,
            publication_id="publication-001",
            expected_revision=1,
            target_phase=Phase.PREPARED,
        )

    assert len(store.events) == 2
    assert store.events[0] == (
        "read",
        "publication-001",
    )
    assert store.events[1][0] == "compare_and_swap"
    assert store.events[1][1] == 1


def test_cas_conflict_is_not_retried_implicitly() -> None:
    store = RecordingStateStore(
        state=create_state(revision=1),
        swap_result=False,
    )

    with pytest.raises(ValueError):
        apply_transition(
            state_store=store,
            publication_id="publication-001",
            expected_revision=1,
            target_phase=Phase.PREPARED,
        )

    assert sum(
        event[0] == "compare_and_swap"
        for event in store.events
    ) == 1
    assert sum(
        event[0] == "read"
        for event in store.events
    ) == 1


def test_store_returning_different_publication_fails_closed() -> None:
    store = RecordingStateStore(
        state=create_state(
            publication_id="publication-002",
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "state_store returned a different "
            "publication_id"
        ),
    ):
        apply_transition(
            state_store=store,
            publication_id="publication-001",
            expected_revision=1,
            target_phase=Phase.PREPARED,
        )

    assert len(store.events) == 1
    assert store.events[0][0] == "read"


@pytest.mark.parametrize(
    "invalid_state",
    (
        object(),
        "state",
        1,
        (),
    ),
)
def test_invalid_store_read_result_fails_closed(
    invalid_state: object,
) -> None:
    store = RecordingStateStore(
        state=invalid_state,
    )

    with pytest.raises(
        TypeError,
        match=(
            "state_store.read must return a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationState or None"
        ),
    ):
        apply_transition(
            state_store=store,
            publication_id="publication-001",
            expected_revision=1,
            target_phase=Phase.PREPARED,
        )

    assert len(store.events) == 1


@pytest.mark.parametrize(
    "invalid_result",
    (
        None,
        0,
        1,
        "",
        (),
        object(),
    ),
)
def test_cas_requires_exact_boolean_result(
    invalid_result: object,
) -> None:
    store = RecordingStateStore(
        state=create_state(),
        swap_result=invalid_result,
    )

    with pytest.raises(
        TypeError,
        match=(
            "state_store.compare_and_swap "
            "must return a bool"
        ),
    ):
        apply_transition(
            state_store=store,
            publication_id="publication-001",
            expected_revision=1,
            target_phase=Phase.PREPARED,
        )


def test_read_backend_failure_propagates() -> None:
    store = RecordingStateStore(
        state=None,
        read_failure=RuntimeError("read unavailable"),
    )

    with pytest.raises(
        RuntimeError,
        match="read unavailable",
    ):
        apply_transition(
            state_store=store,
            publication_id="publication-001",
            expected_revision=1,
            target_phase=Phase.PREPARED,
        )

    assert len(store.events) == 1
    assert store.events[0][0] == "read"


def test_cas_backend_failure_propagates() -> None:
    store = RecordingStateStore(
        state=create_state(),
        swap_failure=RuntimeError("write unavailable"),
    )

    with pytest.raises(
        RuntimeError,
        match="write unavailable",
    ):
        apply_transition(
            state_store=store,
            publication_id="publication-001",
            expected_revision=1,
            target_phase=Phase.PREPARED,
        )

    assert len(store.events) == 2


@pytest.mark.parametrize(
    "invalid_store",
    (
        None,
        object(),
        "store",
        1,
        (),
    ),
)
def test_state_store_requires_complete_protocol(
    invalid_store: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="state_store must implement",
    ):
        apply_transition(
            state_store=invalid_store,
            publication_id="publication-001",
            expected_revision=1,
            target_phase=Phase.PREPARED,
        )


@pytest.mark.parametrize(
    "invalid_id",
    (
        None,
        object(),
        1,
        b"publication-001",
        (),
    ),
)
def test_publication_id_requires_exact_string(
    invalid_id: object,
) -> None:
    store = RecordingStateStore(
        state=create_state(),
    )

    with pytest.raises(
        TypeError,
        match="publication_id must be a string",
    ):
        apply_transition(
            state_store=store,
            publication_id=invalid_id,
            expected_revision=1,
            target_phase=Phase.PREPARED,
        )

    assert store.events == []


def test_publication_id_rejects_empty_value() -> None:
    store = RecordingStateStore(
        state=create_state(),
    )

    with pytest.raises(
        ValueError,
        match="publication_id must not be empty",
    ):
        apply_transition(
            state_store=store,
            publication_id="",
            expected_revision=1,
            target_phase=Phase.PREPARED,
        )

    assert store.events == []


@pytest.mark.parametrize(
    "invalid_revision",
    (
        None,
        True,
        False,
        1.0,
        "1",
        (),
    ),
)
def test_expected_revision_requires_exact_integer(
    invalid_revision: object,
) -> None:
    store = RecordingStateStore(
        state=create_state(),
    )

    with pytest.raises(
        TypeError,
        match="expected_revision",
    ):
        apply_transition(
            state_store=store,
            publication_id="publication-001",
            expected_revision=invalid_revision,
            target_phase=Phase.PREPARED,
        )

    assert store.events == []


@pytest.mark.parametrize(
    "invalid_revision",
    (
        0,
        -1,
        UINT64_MAX + 1,
    ),
)
def test_expected_revision_requires_positive_uint64(
    invalid_revision: int,
) -> None:
    store = RecordingStateStore(
        state=create_state(),
    )

    with pytest.raises(
        ValueError,
        match="expected_revision",
    ):
        apply_transition(
            state_store=store,
            publication_id="publication-001",
            expected_revision=invalid_revision,
            target_phase=Phase.PREPARED,
        )

    assert store.events == []


@pytest.mark.parametrize(
    "invalid_phase",
    (
        None,
        object(),
        "PREPARED",
        1,
        (),
    ),
)
def test_target_phase_requires_nominal_type(
    invalid_phase: object,
) -> None:
    store = RecordingStateStore(
        state=create_state(),
    )

    with pytest.raises(
        TypeError,
        match="target_phase must be a",
    ):
        apply_transition(
            state_store=store,
            publication_id="publication-001",
            expected_revision=1,
            target_phase=invalid_phase,
        )

    assert store.events == []


def test_revision_overflow_fails_before_cas() -> None:
    store = RecordingStateStore(
        state=create_state(
            phase=Phase.INTENT_RECORDED,
            revision=UINT64_MAX,
        ),
    )

    with pytest.raises(
        ValueError,
        match="publication revision cannot exceed uint64",
    ):
        apply_transition(
            state_store=store,
            publication_id="publication-001",
            expected_revision=UINT64_MAX,
            target_phase=Phase.PREPARED,
        )

    assert len(store.events) == 1
    assert store.events[0][0] == "read"


def test_application_never_calls_create() -> None:
    store = RecordingStateStore(
        state=create_state(),
    )

    apply_transition(
        state_store=store,
        publication_id="publication-001",
        expected_revision=1,
        target_phase=Phase.PREPARED,
    )

    assert all(
        event[0] != "create"
        for event in store.events
    )
