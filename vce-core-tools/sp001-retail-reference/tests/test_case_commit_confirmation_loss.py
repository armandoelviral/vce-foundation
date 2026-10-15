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
def test_persisted_commit_survives_lost_confirmation_without_duplicate(
    tmp_path, operation,
):
    path = tmp_path / "case.sqlite3"
    enabled = [False]
    calls = []
    observations = []
    injected = sqlite3.OperationalError("controlled post-commit delivery failure")
    injected.sqlite_errorcode = sqlite3.SQLITE_IOERR

    class Probe:
        def __init__(self, connection):
            self.connection = connection

        def execute(self, sql, *args):
            normalized = " ".join(sql.split()).upper()
            calls.append(normalized)
            result = self.connection.execute(sql, *args)
            if normalized == "COMMIT":
                # The real SQLite COMMIT already returned successfully.
                assert not self.connection.in_transaction
                raise injected
            return result

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
            pause_ns=1_000_000,
        ),
    )
    if operation == "compare_and_swap":
        assert store.create(state=make_state(), transition=make_transition())

    observations.clear()
    enabled[0] = True
    with pytest.raises(sqlite3.OperationalError) as caught:
        invoke(store, operation, perf_counter_ns() + 10_000_000_000)
    enabled[0] = False

    assert caught.value is injected
    assert calls.count("BEGIN IMMEDIATE") == 1
    assert calls.count("COMMIT") == 1
    assert "ROLLBACK" not in calls

    reopened = SqliteCaseAuthoritativeStateStore(
        database_path=path,
        write_acquisition=SpacedSqliteWriteAcquisition(
            pause_ns=1_000_000,
        ),
    )
    expected_revision = 1 if operation == "create" else 2
    state = reopened.read(case_id="CASE-001")
    history = reopened.read_transitions(case_id="CASE-001")
    assert state is not None
    assert state.revision == expected_revision
    assert len(history) == expected_revision
    assert history[-1].revision == state.revision
    assert history[-1].to_phase is state.phase

    # The wrapper withheld confirmation from the measurement as well.
    # committed=False is therefore not proof that persistence did not occur.
    assert len(observations) == 1
    value = observations[0]
    assert value.failed
    assert not value.committed
    assert value.commit_ns is not None
    assert value.rollback_ns is None

    # Repeat the exact create or CAS request with a fresh deadline.
    # False means not applied again; it does not reconstruct original success.
    assert invoke(
        reopened, operation, perf_counter_ns() + 2_000_000_000,
    ) is False
    assert reopened.read(case_id="CASE-001") == state
    assert reopened.read_transitions(case_id="CASE-001") == history

    # A subsequent independent write still works.
    from dataclasses import replace
    recovery_state = replace(make_state(), case_id="RECOVERY")
    recovery_transition = replace(
        make_transition(), case_id="RECOVERY",
        transition_id="RECOVERY-TRANSITION",
    )
    assert reopened.create(
        state=recovery_state,
        transition=recovery_transition,
        write_deadline_ns=perf_counter_ns() + 2_000_000_000,
    )
    assert reopened.read(case_id="RECOVERY") == recovery_state
    assert reopened.read_transitions(case_id="RECOVERY") == (
        recovery_transition,
    )
