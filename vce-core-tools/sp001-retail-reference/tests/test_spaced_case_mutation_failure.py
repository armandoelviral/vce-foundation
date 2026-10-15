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
def test_mutation_failure_rolls_back_without_retry_and_recovers(
    tmp_path, operation,
):
    path = tmp_path / "case.sqlite3"
    calls = []
    waits = []
    observations = []
    injected = sqlite3.OperationalError("controlled mutation failure")
    injected.sqlite_errorcode = sqlite3.SQLITE_BUSY

    class Probe:
        def __init__(self, connection):
            self.connection = connection

        def execute(self, sql, *args):
            normalized = " ".join(sql.split()).upper()
            calls.append(normalized)
            if normalized.startswith("INSERT INTO CASE_LIFECYCLE_TRANSITIONS"):
                raise injected
            return self.connection.execute(sql, *args)

        def __getattr__(self, name):
            return getattr(self.connection, name)

    class Store(SqliteCaseAuthoritativeStateStore):
        def _connect(self):
            connection = super()._connect()
            return Probe(connection) if enabled[0] else connection

    enabled = [False]
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
    assert calls.count("ROLLBACK") == 1
    assert "COMMIT" not in calls

    state_mutations = [
        sql for sql in calls
        if sql.startswith("INSERT INTO CASE_AUTHORITATIVE_STATES")
        or sql.startswith("UPDATE CASE_AUTHORITATIVE_STATES")
    ]
    history_mutations = [
        sql for sql in calls
        if sql.startswith("INSERT INTO CASE_LIFECYCLE_TRANSITIONS")
    ]
    assert len(state_mutations) == 1
    assert len(history_mutations) == 1
    assert (
        store.read(case_id="CASE-001"),
        store.read_transitions(case_id="CASE-001"),
    ) == baseline

    assert len(observations) == 1
    value = observations[0]
    assert value.failed and not value.committed
    assert value.begin_ns is not None
    assert value.rollback_ns is not None
    assert value.commit_ns is None

    assert invoke(store, operation, perf_counter_ns() + 2_000_000_000)
    reopened = SqliteCaseAuthoritativeStateStore(database_path=path)
    expected_revision = 1 if operation == "create" else 2
    assert reopened.read(case_id="CASE-001").revision == expected_revision
    assert len(reopened.read_transitions(case_id="CASE-001")) == expected_revision
