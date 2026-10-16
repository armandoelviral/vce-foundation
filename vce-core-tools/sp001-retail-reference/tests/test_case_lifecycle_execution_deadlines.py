import sqlite3
from threading import Event, Thread
from time import perf_counter_ns

import pytest

from test_case_lifecycle_completion import opening, completion
from sp001.contracts.case_authoritative_state_store import (
    CaseWriteDeadlineExceeded,
)
from sp001.infrastructure.sqlite_case_lifecycle_execution import (
    SqliteCaseLifecycleExecutionStore,
)
from sp001.infrastructure.sqlite_write_acquisition import (
    SpacedSqliteWriteAcquisition,
)
import sp001.services.sqlite_case_authoritative_state_store as state_module


def acquisition(spaced):
    return (
        SpacedSqliteWriteAcquisition(pause_ns=1_000_000)
        if spaced else None
    )


def prepare(store, operation):
    if operation == "transition":
        assert store.execute(request=opening().request) == opening()
        return completion()
    return opening()


def snapshot(store):
    return (
        store.read(case_id="CASE-1"),
        store.read_transitions(case_id="CASE-1"),
    )


@pytest.mark.parametrize("operation", ["opening", "transition"])
@pytest.mark.parametrize("spaced", [False, True])
def test_lock_expiry_leaves_no_partial_effect_and_retry_recovers(
    tmp_path, operation, spaced,
):
    path = tmp_path / "case.sqlite3"
    observations = []
    store = SqliteCaseLifecycleExecutionStore(
        database_path=path, write_acquisition=acquisition(spaced),
        write_observer=observations.append,
    )
    expected = prepare(store, operation)
    baseline = snapshot(store)
    observations.clear()
    finished = Event()
    errors = []

    def work():
        try:
            store.execute(
                request=expected.request,
                write_deadline_ns=perf_counter_ns() + 80_000_000,
            )
        except BaseException as error:
            errors.append(error)
        finally:
            finished.set()

    blocker = sqlite3.connect(path, isolation_level=None, timeout=0)
    worker = Thread(target=work)
    try:
        blocker.execute("BEGIN IMMEDIATE")
        worker.start()
        # Watchdog, not an 80 ms return-time guarantee.
        assert finished.wait(3)
        assert len(errors) == 1
        assert isinstance(errors[0], CaseWriteDeadlineExceeded)
        assert snapshot(store) == baseline
        assert store.recover(request=expected.request) is None
    finally:
        if blocker.in_transaction:
            blocker.execute("ROLLBACK")
        blocker.close()
        if worker.ident is not None:
            worker.join(7)

    assert not worker.is_alive()
    assert len(observations) == 1
    value = observations[0]
    assert value.failed and not value.committed
    assert value.commit_ns is None
    assert value.rollback_ns is None

    assert store.execute(
        request=expected.request,
        write_deadline_ns=perf_counter_ns() + 2_000_000_000,
    ) == expected
    assert store.recover(request=expected.request) == expected


@pytest.mark.parametrize("operation", ["opening", "transition"])
@pytest.mark.parametrize("spaced", [False, True])
def test_expiry_after_completion_insert_rolls_back_everything(
    tmp_path, monkeypatch, operation, spaced,
):
    path = tmp_path / "case.sqlite3"
    enabled = [False]
    now = [1_000_000_000]
    deadline = 2_000_000_000
    calls = []
    observations = []

    class Probe:
        def __init__(self, connection):
            self.connection = connection

        def execute(self, sql, *args):
            normalized = " ".join(sql.split()).upper()
            calls.append(normalized)
            result = self.connection.execute(sql, *args)
            if normalized.startswith("INSERT INTO CASE_LIFECYCLE_COMPLETIONS"):
                # All three writes happened, but none has committed.
                assert self.connection.in_transaction
                now[0] = deadline
            return result

        def __getattr__(self, name):
            return getattr(self.connection, name)

    class Store(SqliteCaseLifecycleExecutionStore):
        def _connect(self):
            connection = super()._connect()
            return Probe(connection) if enabled[0] else connection

    option = (
        SpacedSqliteWriteAcquisition(
            pause_ns=1_000_000, clock=lambda: now[0],
        ) if spaced else None
    )
    store = Store(
        database_path=path, write_acquisition=option,
        write_observer=observations.append,
    )
    expected = prepare(store, operation)
    baseline = snapshot(store)
    observations.clear()
    monkeypatch.setattr(state_module, "perf_counter_ns", lambda: now[0])
    enabled[0] = True

    with pytest.raises(CaseWriteDeadlineExceeded):
        store.execute(
            request=expected.request, write_deadline_ns=deadline,
        )
    enabled[0] = False

    assert calls.count("BEGIN IMMEDIATE") == 1
    assert calls.count("ROLLBACK") == 1
    assert "COMMIT" not in calls
    assert sum(
        sql.startswith("INSERT INTO CASE_LIFECYCLE_COMPLETIONS")
        for sql in calls
    ) == 1

    reopened = SqliteCaseLifecycleExecutionStore(database_path=path)
    assert snapshot(reopened) == baseline
    assert reopened.recover(request=expected.request) is None
    assert len(observations) == 1
    value = observations[0]
    assert value.failed and not value.committed
    assert value.commit_ns is None
    assert value.rollback_ns is not None

    assert store.execute(
        request=expected.request,
        write_deadline_ns=deadline + 1_000_000_000,
    ) == expected
    assert reopened.recover(request=expected.request) == expected
