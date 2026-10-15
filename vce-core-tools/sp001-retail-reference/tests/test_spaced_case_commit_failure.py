import sqlite3
from time import perf_counter_ns

import pytest

from test_case_state_write_deadline import invoke
from test_sqlite_case_authoritative_state_store import make_state, make_transition
from sp001.infrastructure.sqlite_write_acquisition import (
    SpacedSqliteWriteAcquisition,
)
from sp001.services.sqlite_case_authoritative_state_store import (
    SqliteCaseAuthoritativeStateStore,
)


@pytest.mark.parametrize("operation", ["create", "compare_and_swap"])
def test_commit_failure_is_not_retried_and_active_transaction_rolls_back(
    tmp_path, operation,
):
    path = tmp_path / "case.sqlite3"
    enabled = [False]
    calls = []
    waits = []
    observations = []
    injected = sqlite3.OperationalError("controlled pre-commit failure")
    injected.sqlite_errorcode = sqlite3.SQLITE_BUSY

    class Probe:
        def __init__(self, connection):
            self.connection = connection

        def execute(self, sql, *args):
            normalized = " ".join(sql.split()).upper()
            calls.append(normalized)
            if normalized == "COMMIT":
                assert self.connection.in_transaction
                raise injected
            return self.connection.execute(sql, *args)

        def __getattr__(self, name):
            return getattr(self.connection, name)

    class Store(SqliteCaseAuthoritativeStateStore):
        def _connect(self):
            connection = super()._connect()
            return Probe(connection) if enabled[0] else connection

    store = Store(
        database_path=path,
        write_observer=observations.append,
        write_acquisition=SpacedSqliteWriteAcquisition(
            pause_ns=1_000_000, wait=waits.append,
        ),
    )
    if operation == "compare_and_swap":
        assert store.create(state=make_state(), transition=make_transition())

    baseline = (
        store.read(case_id="CASE-001"),
        store.read_transitions(case_id="CASE-001"),
    )
    observations.clear()
    enabled[0] = True

    with pytest.raises(sqlite3.OperationalError) as caught:
        invoke(store, operation, perf_counter_ns() + 10_000_000_000)

    enabled[0] = False
    assert caught.value is injected
    assert waits == []
    assert calls.count("BEGIN IMMEDIATE") == 1
    assert calls.count("COMMIT") == 1
    assert calls.count("ROLLBACK") == 1
    assert calls.index("COMMIT") < calls.index("ROLLBACK")
    assert sum(
        sql.startswith("INSERT INTO CASE_AUTHORITATIVE_STATES")
        or sql.startswith("UPDATE CASE_AUTHORITATIVE_STATES")
        for sql in calls
    ) == 1
    assert sum(
        sql.startswith("INSERT INTO CASE_LIFECYCLE_TRANSITIONS")
        for sql in calls
    ) == 1

    reopened = SqliteCaseAuthoritativeStateStore(database_path=path)
    assert (
        reopened.read(case_id="CASE-001"),
        reopened.read_transitions(case_id="CASE-001"),
    ) == baseline

    assert len(observations) == 1
    value = observations[0]
    assert value.failed and not value.committed
    assert value.begin_ns is not None
    assert value.commit_ns is not None
    assert value.rollback_ns is not None

    assert invoke(store, operation, perf_counter_ns() + 2_000_000_000)
    expected_revision = 1 if operation == "create" else 2
    assert reopened.read(case_id="CASE-001").revision == expected_revision
    assert len(reopened.read_transitions(case_id="CASE-001")) == expected_revision
