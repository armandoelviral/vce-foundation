import sqlite3
from concurrent.futures import ThreadPoolExecutor

import pytest

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_authoritative_state_store import (
    CaseAuthoritativeStateStore,
)
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase as Phase
from sp001.contracts.case_lifecycle_transition_record import (
    CaseLifecycleTransitionRecord,
)
from sp001.contracts.case_resource_link import CaseResourceLink
from sp001.services.sqlite_case_authoritative_state_store import (
    SqliteCaseAuthoritativeStateStore,
)


def make_link(
    relationship: str = "recommendation",
    resource_type: str = "recommendation",
    resource_id: str = "REC-001",
) -> CaseResourceLink:
    return CaseResourceLink(
        relationship=relationship,
        resource_type=resource_type,
        resource_id=resource_id,
    )


def make_state(
    *,
    phase: Phase = Phase.CASE_OPENED,
    revision: int = 1,
    links: tuple[CaseResourceLink, ...] = (),
) -> CaseAuthoritativeState:
    return CaseAuthoritativeState(
        case_id="CASE-001",
        objective_id="OBJ-001",
        scope="STORE-MX-014",
        phase=phase,
        revision=revision,
        resource_links=links,
    )


def make_transition(
    *,
    revision: int = 1,
    from_phase: Phase | None = None,
    to_phase: Phase = Phase.CASE_OPENED,
    links: tuple[CaseResourceLink, ...] = (),
    transition_id: str | None = None,
) -> CaseLifecycleTransitionRecord:
    return CaseLifecycleTransitionRecord(
        case_id="CASE-001",
        transition_id=transition_id or f"TRANSITION-{revision}",
        revision=revision,
        from_phase=from_phase,
        to_phase=to_phase,
        resource_links=links,
    )


def store(path) -> SqliteCaseAuthoritativeStateStore:
    return SqliteCaseAuthoritativeStateStore(database_path=path)


def test_adapter_implements_store_protocol(tmp_path) -> None:
    assert isinstance(store(tmp_path / "case.sqlite3"), CaseAuthoritativeStateStore)


def test_constructor_creates_wal_database_and_schema(tmp_path) -> None:
    path = tmp_path / "case.sqlite3"
    store(path)
    connection = sqlite3.connect(path)
    try:
        mode = connection.execute("PRAGMA journal_mode").fetchone()[0]
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
    finally:
        connection.close()
    assert mode.lower() == "wal"
    assert "case_authoritative_states" in tables
    assert "case_lifecycle_transitions" in tables


def test_missing_case_and_history_are_empty(tmp_path) -> None:
    adapter = store(tmp_path / "case.sqlite3")
    assert adapter.read(case_id="CASE-MISSING") is None
    assert adapter.read_transitions(case_id="CASE-MISSING") == ()


def test_create_and_read_preserve_state_and_initial_transition(tmp_path) -> None:
    adapter = store(tmp_path / "case.sqlite3")
    expected = make_state()
    initial = make_transition()
    assert adapter.create(state=expected, transition=initial)
    assert adapter.read(case_id="CASE-001") == expected
    assert adapter.read_transitions(case_id="CASE-001") == (initial,)


def test_duplicate_create_preserves_original(tmp_path) -> None:
    adapter = store(tmp_path / "case.sqlite3")
    original = make_state()
    assert adapter.create(state=original, transition=make_transition())
    changed = make_state(phase=Phase.RECOMMENDATION_AVAILABLE)
    changed_transition = make_transition(
        to_phase=Phase.RECOMMENDATION_AVAILABLE,
        transition_id="TRANSITION-DUPLICATE",
    )
    assert not adapter.create(state=changed, transition=changed_transition)
    assert adapter.read(case_id="CASE-001") == original
    assert len(adapter.read_transitions(case_id="CASE-001")) == 1


def test_state_and_history_survive_a_new_store_instance(tmp_path) -> None:
    path = tmp_path / "case.sqlite3"
    first = store(path)
    state1 = make_state()
    transition1 = make_transition()
    assert first.create(state=state1, transition=transition1)

    link = make_link()
    state2 = make_state(
        phase=Phase.RECOMMENDATION_AVAILABLE,
        revision=2,
        links=(link,),
    )
    transition2 = make_transition(
        revision=2,
        from_phase=Phase.CASE_OPENED,
        to_phase=Phase.RECOMMENDATION_AVAILABLE,
        links=(link,),
    )
    assert first.compare_and_swap(
        expected_revision=1,
        next_state=state2,
        transition=transition2,
    )

    second = store(path)
    assert second.read(case_id="CASE-001") == state2
    assert second.read_transitions(case_id="CASE-001") == (
        transition1,
        transition2,
    )


def test_stale_compare_and_swap_changes_nothing(tmp_path) -> None:
    adapter = store(tmp_path / "case.sqlite3")
    initial = make_state()
    initial_transition = make_transition()
    assert adapter.create(state=initial, transition=initial_transition)

    link = make_link()
    next_state = make_state(
        phase=Phase.RECOMMENDATION_AVAILABLE,
        revision=2,
        links=(link,),
    )
    next_transition = make_transition(
        revision=2,
        from_phase=Phase.CASE_OPENED,
        to_phase=Phase.RECOMMENDATION_AVAILABLE,
        links=(link,),
    )
    assert not adapter.compare_and_swap(
        expected_revision=7,
        next_state=next_state,
        transition=next_transition,
    )
    assert adapter.read(case_id="CASE-001") == initial
    assert adapter.read_transitions(case_id="CASE-001") == (
        initial_transition,
    )


def test_compare_and_swap_requires_exact_successor_revision(tmp_path) -> None:
    adapter = store(tmp_path / "case.sqlite3")
    initial = make_state()
    assert adapter.create(state=initial, transition=make_transition())

    invalid_state = make_state(
        phase=Phase.RECOMMENDATION_AVAILABLE,
        revision=3,
    )
    invalid_transition = make_transition(
        revision=3,
        from_phase=Phase.CASE_OPENED,
        to_phase=Phase.RECOMMENDATION_AVAILABLE,
    )
    with pytest.raises(ValueError, match="exact successor"):
        adapter.compare_and_swap(
            expected_revision=1,
            next_state=invalid_state,
            transition=invalid_transition,
        )
    assert adapter.read(case_id="CASE-001") == initial


def test_compare_and_swap_rejects_transition_source_mismatch(tmp_path) -> None:
    adapter = store(tmp_path / "case.sqlite3")
    initial = make_state()
    assert adapter.create(state=initial, transition=make_transition())

    next_state = make_state(
        phase=Phase.RECOMMENDATION_AVAILABLE,
        revision=2,
    )
    wrong_transition = make_transition(
        revision=2,
        from_phase=Phase.AWAITING_EXPERT_DECISION,
        to_phase=Phase.RECOMMENDATION_AVAILABLE,
    )
    with pytest.raises(ValueError, match="source"):
        adapter.compare_and_swap(
            expected_revision=1,
            next_state=next_state,
            transition=wrong_transition,
        )


def test_two_concurrent_writers_have_one_winner(tmp_path) -> None:
    path = tmp_path / "case.sqlite3"
    first = store(path)
    assert first.create(state=make_state(), transition=make_transition())
    second = store(path)

    def advance(adapter, transition_id):
        next_state = make_state(
            phase=Phase.RECOMMENDATION_AVAILABLE,
            revision=2,
        )
        next_transition = make_transition(
            revision=2,
            from_phase=Phase.CASE_OPENED,
            to_phase=Phase.RECOMMENDATION_AVAILABLE,
            transition_id=transition_id,
        )
        return adapter.compare_and_swap(
            expected_revision=1,
            next_state=next_state,
            transition=next_transition,
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = tuple(
            executor.map(
                lambda args: advance(*args),
                (
                    (first, "TRANSITION-A"),
                    (second, "TRANSITION-B"),
                ),
            )
        )

    assert sorted(results) == [False, True]
    assert first.read(case_id="CASE-001").revision == 2
    assert len(first.read_transitions(case_id="CASE-001")) == 2


def test_transition_insert_failure_rolls_back_state_update(tmp_path) -> None:
    path = tmp_path / "case.sqlite3"
    adapter = store(path)
    initial = make_state()
    initial_transition = make_transition()
    assert adapter.create(state=initial, transition=initial_transition)

    connection = sqlite3.connect(path)
    try:
        connection.execute(
            """
            CREATE TRIGGER reject_case_transition
            BEFORE INSERT ON case_lifecycle_transitions
            WHEN NEW.revision = '00000000000000000002'
            BEGIN
                SELECT RAISE(ABORT, 'forced transition failure');
            END
            """
        )
        connection.commit()
    finally:
        connection.close()

    next_state = make_state(
        phase=Phase.RECOMMENDATION_AVAILABLE,
        revision=2,
    )
    next_transition = make_transition(
        revision=2,
        from_phase=Phase.CASE_OPENED,
        to_phase=Phase.RECOMMENDATION_AVAILABLE,
    )
    assert not adapter.compare_and_swap(
        expected_revision=1,
        next_state=next_state,
        transition=next_transition,
    )
    assert adapter.read(case_id="CASE-001") == initial
    assert adapter.read_transitions(case_id="CASE-001") == (
        initial_transition,
    )
