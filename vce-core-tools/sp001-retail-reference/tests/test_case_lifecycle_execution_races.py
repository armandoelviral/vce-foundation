import sqlite3
from dataclasses import replace
from threading import Event, Thread
from time import perf_counter_ns

import pytest

from test_case_lifecycle_completion import opening, completion
from sp001.contracts.case_lifecycle_execution_store import (
    CaseLifecycleRequestConflict,
)
from sp001.infrastructure.sqlite_case_lifecycle_execution import (
    SqliteCaseLifecycleExecutionStore,
)
from sp001.infrastructure.sqlite_write_acquisition import (
    SpacedSqliteWriteAcquisition,
)


@pytest.mark.parametrize("workers", [4, 8])
@pytest.mark.parametrize("operation", ["opening", "transition"])
@pytest.mark.parametrize("contradictory", [False, True])
def test_same_identity_race_preserves_one_exact_completion(
    tmp_path, workers, operation, contradictory,
):
    path = tmp_path / "case.sqlite3"
    initial = SqliteCaseLifecycleExecutionStore(database_path=path)
    if operation == "transition":
        initial.execute(request=opening().request)
        base = completion().request
        previous_count = 1
    else:
        base = opening().request
        previous_count = 0

    requests = []
    for index in range(workers):
        if not contradictory:
            request_value = replace(base)
        elif operation == "opening":
            request_value = replace(base, scope=f"STORE-{index}")
        else:
            added = replace(
                base.resource_links[0], resource_id=f"RECEIPT-{index}",
            )
            request_value = replace(base, resource_links=(added,))
        requests.append(request_value)

    attempted = [Event() for _ in range(workers)]
    finished = [Event() for _ in range(workers)]
    start = Event()
    results = [None] * workers
    conflicts = [None] * workers
    errors = [None] * workers
    adapters = []

    # Initialize schemas before acquiring the external blocker.
    for index in range(workers):
        def wait(seconds, index=index):
            attempted[index].set()
            Event().wait(seconds)

        adapters.append(SqliteCaseLifecycleExecutionStore(
            database_path=path,
            write_acquisition=SpacedSqliteWriteAcquisition(
                pause_ns=1_000_000, wait=wait,
            ),
        ))

    def work(index):
        start.wait()
        try:
            results[index] = adapters[index].execute(
                request=requests[index],
                write_deadline_ns=perf_counter_ns() + 10_000_000_000,
            )
        except CaseLifecycleRequestConflict as error:
            conflicts[index] = error
        except BaseException as error:
            errors[index] = error
        finally:
            finished[index].set()

    threads = [Thread(target=work, args=(i,)) for i in range(workers)]
    blocker = sqlite3.connect(path, isolation_level=None, timeout=0)
    try:
        blocker.execute("BEGIN IMMEDIATE")
        for thread in threads:
            thread.start()
        start.set()

        # Every contender must observe real SQLite BUSY before release.
        for event in attempted:
            assert event.wait(3), "contender did not observe BUSY"
        assert all(not event.is_set() for event in finished)
        blocker.execute("ROLLBACK")

        watchdog = perf_counter_ns() + 12_000_000_000
        for event in finished:
            assert event.wait(
                max(0, watchdog - perf_counter_ns()) / 1_000_000_000
            ), "contender did not finish"
    finally:
        start.set()
        if blocker.in_transaction:
            blocker.execute("ROLLBACK")
        blocker.close()
        for thread in threads:
            if thread.ident is not None:
                thread.join(12)

    assert all(not thread.is_alive() for thread in threads)
    assert errors == [None] * workers
    completed = [result for result in results if result is not None]
    assert completed
    winner = completed[0]

    if contradictory:
        assert len(completed) == 1
        assert sum(error is not None for error in conflicts) == workers - 1
        winner_index = next(
            i for i, result in enumerate(results) if result is not None
        )
        assert winner.request == requests[winner_index]
    else:
        assert len(completed) == workers
        assert conflicts == [None] * workers
        assert all(result == winner for result in completed)

    reopened = SqliteCaseLifecycleExecutionStore(database_path=path)
    assert reopened.read(case_id=base.case_id) == winner.state
    history = reopened.read_transitions(case_id=base.case_id)
    assert len(history) == previous_count + 1
    assert history[-1] == winner.transition
    if operation == "transition":
        assert history[0] == opening().transition
        assert winner.previous_state == opening().state

    # Repeated recovery/execution must not overwrite the winning result.
    for request_value in requests:
        if request_value == winner.request:
            assert reopened.recover(request=request_value) == winner
            assert reopened.execute(request=request_value) == winner
        else:
            for method in (reopened.recover, reopened.execute):
                with pytest.raises(CaseLifecycleRequestConflict):
                    method(request=request_value)

    assert reopened.read(case_id=base.case_id) == winner.state
    assert reopened.read_transitions(case_id=base.case_id) == history

    connection = sqlite3.connect(path)
    try:
        assert connection.execute(
            "SELECT COUNT(*) FROM case_authoritative_states"
        ).fetchone()[0] == 1
        assert connection.execute(
            "SELECT COUNT(*) FROM case_lifecycle_transitions"
        ).fetchone()[0] == previous_count + 1
        assert connection.execute(
            "SELECT COUNT(*) FROM case_lifecycle_completions"
        ).fetchone()[0] == previous_count + 1
        assert connection.execute(
            """SELECT COUNT(*) FROM case_lifecycle_completions
            WHERE transition_id=?""",
            (base.transition_id,),
        ).fetchone()[0] == 1
    finally:
        connection.close()
