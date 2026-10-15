import sqlite3
from threading import Event, Thread
from time import perf_counter_ns

import pytest

from test_sqlite_case_authoritative_state_store import make_state, make_transition
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase as Phase
from sp001.infrastructure.sqlite_write_acquisition import (
    SpacedSqliteWriteAcquisition,
)
from sp001.services.sqlite_case_authoritative_state_store import (
    SqliteCaseAuthoritativeStateStore,
)


@pytest.mark.parametrize("workers", [4, 8])
def test_released_lock_allows_exactly_one_revision_winner(tmp_path, workers):
    path = tmp_path / "case.sqlite3"
    attempted = [Event() for _ in range(workers)]
    finished = [Event() for _ in range(workers)]
    start = Event()
    outcomes = [None] * workers
    errors = [None] * workers

    adapters = []

    def contender(index):
        store = adapters[index]
        start.wait()
        try:
            outcomes[index] = store.compare_and_swap(
                expected_revision=1,
                next_state=make_state(
                    phase=Phase.RECOMMENDATION_AVAILABLE, revision=2,
                ),
                transition=make_transition(
                    revision=2,
                    from_phase=Phase.CASE_OPENED,
                    to_phase=Phase.RECOMMENDATION_AVAILABLE,
                    transition_id=f"RACE-{index}",
                ),
                write_deadline_ns=perf_counter_ns() + 5_000_000_000,
            )
        except BaseException as error:
            errors[index] = error
        finally:
            finished[index].set()

    store = SqliteCaseAuthoritativeStateStore(database_path=path)
    assert store.create(state=make_state(), transition=make_transition())
    original_history = store.read_transitions(case_id="CASE-001")

    for index in range(workers):
        def wait(seconds, index=index):
            attempted[index].set()
            Event().wait(seconds)

        adapters.append(SqliteCaseAuthoritativeStateStore(
            database_path=path,
            write_acquisition=SpacedSqliteWriteAcquisition(
                pause_ns=1_000_000, wait=wait,
            ),
        ))

    threads = [Thread(target=contender, args=(i,)) for i in range(workers)]
    blocker = sqlite3.connect(path, isolation_level=None, timeout=0)
    try:
        for thread in threads:
            thread.start()
        blocker.execute("BEGIN IMMEDIATE")
        start.set()

        for event in attempted:
            assert event.wait(3), "contender did not observe BUSY"
        assert all(not event.is_set() for event in finished)

        blocker.execute("ROLLBACK")
        for event in finished:
            assert event.wait(7), "contender did not finish"
    finally:
        start.set()
        if blocker.in_transaction:
            blocker.execute("ROLLBACK")
        blocker.close()
        for thread in threads:
            if thread.ident is not None:
                thread.join(7)

    assert all(not thread.is_alive() for thread in threads)
    assert errors == [None] * workers
    assert outcomes.count(True) == 1
    assert outcomes.count(False) == workers - 1

    winner = outcomes.index(True)
    reopened = SqliteCaseAuthoritativeStateStore(database_path=path)
    state = reopened.read(case_id="CASE-001")
    history = reopened.read_transitions(case_id="CASE-001")
    assert state.revision == 2
    assert state.phase is Phase.RECOMMENDATION_AVAILABLE
    assert len(history) == 2
    assert history[0] == original_history[0]
    assert history[1].transition_id == f"RACE-{winner}"
    assert history[1].revision == 2
    assert history[1].from_phase is Phase.CASE_OPENED
    assert history[1].to_phase is state.phase
