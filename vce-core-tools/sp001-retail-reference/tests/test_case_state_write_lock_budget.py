import sqlite3
from threading import Event, Thread
from time import perf_counter_ns

import pytest

from test_case_state_write_deadline import invoke
from test_sqlite_case_authoritative_state_store import make_state, make_transition
from sp001.contracts.case_authoritative_state_store import (
    CaseWriteDeadlineExceeded,
)
from sp001.services.sqlite_case_authoritative_state_store import (
    SqliteCaseAuthoritativeStateStore,
)


@pytest.mark.parametrize("operation", ["create", "compare_and_swap"])
def test_lock_wait_finishes_while_blocker_remains_and_retry_succeeds(
    tmp_path, operation,
):
    path = tmp_path / "case.sqlite3"
    observations = []
    store = SqliteCaseAuthoritativeStateStore(
        database_path=path, write_observer=observations.append,
    )
    if operation == "compare_and_swap":
        assert store.create(state=make_state(), transition=make_transition())
    baseline = (
        store.read(case_id="CASE-001"),
        store.read_transitions(case_id="CASE-001"),
    )
    observations.clear()
    finished = Event()
    errors = []

    def work():
        try:
            invoke(store, operation, perf_counter_ns() + 80_000_000)
        except BaseException as error:
            errors.append(error)
        finally:
            finished.set()

    blocker = sqlite3.connect(path, timeout=0)
    worker = Thread(target=work)
    try:
        blocker.execute("BEGIN IMMEDIATE")
        worker.start()
        # The blocker remains held. This is a watchdog, not an 80 ms SLA.
        assert finished.wait(2)
        assert len(errors) == 1
        assert isinstance(errors[0], CaseWriteDeadlineExceeded)
        assert (
            store.read(case_id="CASE-001"),
            store.read_transitions(case_id="CASE-001"),
        ) == baseline
    finally:
        blocker.rollback()
        blocker.close()
        if worker.ident is not None:
            worker.join(7)

    assert not worker.is_alive()
    assert len(observations) == 1
    value = observations[0]
    assert value.failed and not value.committed
    assert value.commit_ns is None
    assert value.rollback_ns is None  # BEGIN never acquired the write lock.
    assert invoke(store, operation, perf_counter_ns() + 2_000_000_000)


def test_stricter_busy_timeout_preserves_busy_error_before_deadline(tmp_path):
    path = tmp_path / "case.sqlite3"

    class ImmediateStore(SqliteCaseAuthoritativeStateStore):
        def _connect(self):
            connection = super()._connect()
            connection.execute("PRAGMA busy_timeout=0")
            return connection

    store = ImmediateStore(database_path=path)
    blocker = sqlite3.connect(path, timeout=0)
    try:
        blocker.execute("BEGIN IMMEDIATE")
        with pytest.raises(sqlite3.OperationalError) as caught:
            invoke(store, "create", perf_counter_ns() + 10_000_000_000)
        assert caught.value.sqlite_errorcode & 0xff == sqlite3.SQLITE_BUSY
    finally:
        blocker.rollback()
        blocker.close()
    assert store.read(case_id="CASE-001") is None
    assert store.read_transitions(case_id="CASE-001") == ()
