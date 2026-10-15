import sqlite3
from time import perf_counter_ns

import pytest

from test_case_state_write_deadline import invoke
from test_sqlite_case_authoritative_state_store import make_state, make_transition
from sp001.contracts.case_authoritative_state_store import (
    CaseWriteDeadlineExceeded,
)
from sp001.infrastructure.sqlite_write_acquisition import (
    SpacedSqliteWriteAcquisition,
)
from sp001.services.sqlite_case_authoritative_state_store import (
    SqliteCaseAuthoritativeStateStore,
)


def busy_error(code=sqlite3.SQLITE_BUSY):
    error = sqlite3.OperationalError("controlled failure")
    error.sqlite_errorcode = code
    return error


class Connection:
    def __init__(self, errors=()):
        self.in_transaction = False
        self.errors = list(errors)
        self.calls = []
        self.result = object()

    def execute(self, sql):
        self.calls.append(sql)
        if sql == "BEGIN IMMEDIATE":
            if self.errors:
                raise self.errors.pop(0)
            self.in_transaction = True
        return self.result


def test_retries_only_begin_and_clips_wait_to_remaining_budget():
    now = [0]
    waits = []

    def wait(seconds):
        waits.append(seconds)
        now[0] += round(seconds * 1_000_000_000)

    connection = Connection([busy_error(), busy_error()])
    acquisition = SpacedSqliteWriteAcquisition(
        pause_ns=5, clock=lambda: now[0], wait=wait,
    )
    with pytest.raises(CaseWriteDeadlineExceeded):
        acquisition.begin(connection, deadline_ns=9)
    assert waits == [5 / 1_000_000_000, 4 / 1_000_000_000]
    assert connection.calls == [
        "PRAGMA busy_timeout=0", "BEGIN IMMEDIATE", "BEGIN IMMEDIATE",
    ]


def test_busy_then_success_returns_without_mutation_or_commit():
    connection = Connection([busy_error()])
    waits = []
    acquisition = SpacedSqliteWriteAcquisition(
        pause_ns=5, clock=lambda: 0, wait=waits.append,
    )
    assert acquisition.begin(connection, deadline_ns=100) is connection.result
    assert len(waits) == 1
    assert connection.calls == [
        "PRAGMA busy_timeout=0", "BEGIN IMMEDIATE", "BEGIN IMMEDIATE",
    ]


@pytest.mark.parametrize("code", [sqlite3.SQLITE_LOCKED, sqlite3.SQLITE_IOERR])
def test_non_busy_error_is_preserved_without_retry(code):
    error = busy_error(code)
    connection = Connection([error])
    waits = []
    acquisition = SpacedSqliteWriteAcquisition(
        pause_ns=5, clock=lambda: 0, wait=waits.append,
    )
    with pytest.raises(sqlite3.OperationalError) as caught:
        acquisition.begin(connection, deadline_ns=100)
    assert caught.value is error
    assert waits == []
    assert connection.calls.count("BEGIN IMMEDIATE") == 1


def test_expired_deadline_does_not_touch_connection():
    connection = Connection()
    acquisition = SpacedSqliteWriteAcquisition(
        pause_ns=5, clock=lambda: 100,
    )
    with pytest.raises(CaseWriteDeadlineExceeded):
        acquisition.begin(connection, deadline_ns=100)
    assert connection.calls == []


def test_existing_transaction_is_not_retried_or_changed():
    connection = Connection()
    connection.in_transaction = True
    acquisition = SpacedSqliteWriteAcquisition(pause_ns=5)
    with pytest.raises(RuntimeError, match="active transaction"):
        acquisition.begin(connection, deadline_ns=perf_counter_ns() + 1000000)
    assert connection.calls == []


@pytest.mark.parametrize("operation", ["create", "compare_and_swap"])
def test_real_lock_expiry_preserves_state_history_and_recovers(
    tmp_path, operation,
):
    path = tmp_path / "case.sqlite3"
    observations = []
    store = SqliteCaseAuthoritativeStateStore(
        database_path=path,
        write_observer=observations.append,
        write_acquisition=SpacedSqliteWriteAcquisition(pause_ns=1_000_000),
    )
    if operation == "compare_and_swap":
        assert store.create(state=make_state(), transition=make_transition())
    baseline = (
        store.read(case_id="CASE-001"),
        store.read_transitions(case_id="CASE-001"),
    )
    observations.clear()
    blocker = sqlite3.connect(path, isolation_level=None, timeout=0)
    try:
        blocker.execute("BEGIN IMMEDIATE")
        with pytest.raises(CaseWriteDeadlineExceeded):
            invoke(store, operation, perf_counter_ns() + 30_000_000)
        assert (
            store.read(case_id="CASE-001"),
            store.read_transitions(case_id="CASE-001"),
        ) == baseline
    finally:
        blocker.execute("ROLLBACK")
        blocker.close()

    assert len(observations) == 1
    value = observations[0]
    assert value.failed and not value.committed
    assert value.begin_ns is not None
    assert value.commit_ns is None
    assert value.rollback_ns is None
    assert invoke(store, operation, perf_counter_ns() + 2_000_000_000)
    assert len(store.read_transitions(case_id="CASE-001")) == (
        1 if operation == "create" else 2
    )


def test_no_deadline_preserves_existing_acquisition(tmp_path):
    class ForbiddenAcquisition(SpacedSqliteWriteAcquisition):
        def begin(self, connection, *, deadline_ns):
            raise AssertionError("optional acquisition must not be used")

    store = SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3",
        write_acquisition=ForbiddenAcquisition(pause_ns=5),
    )
    assert store.create(state=make_state(), transition=make_transition())


def test_invalid_option_does_not_create_database(tmp_path):
    path = tmp_path / "absent.sqlite3"
    with pytest.raises(TypeError, match="write_acquisition"):
        SqliteCaseAuthoritativeStateStore(
            database_path=path, write_acquisition=object(),
        )
    assert not path.exists()


@pytest.mark.parametrize("pause", [True, 1.5, "5"])
def test_invalid_pause_type(pause):
    with pytest.raises(TypeError):
        SpacedSqliteWriteAcquisition(pause_ns=pause)


@pytest.mark.parametrize("pause", [0, -1])
def test_invalid_pause_value(pause):
    with pytest.raises(ValueError):
        SpacedSqliteWriteAcquisition(pause_ns=pause)
