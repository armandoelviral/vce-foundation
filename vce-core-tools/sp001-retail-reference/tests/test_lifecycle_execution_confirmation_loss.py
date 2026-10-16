import sqlite3
from dataclasses import replace
from time import perf_counter_ns

import pytest

from test_case_lifecycle_completion import opening, completion
from sp001.contracts.case_lifecycle_execution_store import (
    CaseLifecycleRequestConflict,
)
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase as Phase
from sp001.contracts.case_lifecycle_request import CaseTransitionRequest
from sp001.infrastructure.sqlite_case_lifecycle_execution import (
    SqliteCaseLifecycleExecutionStore,
)
from sp001.infrastructure.sqlite_write_acquisition import (
    SpacedSqliteWriteAcquisition,
)


@pytest.mark.parametrize("operation", ["opening", "transition"])
@pytest.mark.parametrize("spaced", [False, True])
def test_lost_confirmation_recovers_original_result_without_duplicate(
    tmp_path, operation, spaced,
):
    path = tmp_path / "case.sqlite3"
    enabled = [False]
    calls = []
    observations = []
    injected = sqlite3.OperationalError("controlled lost commit confirmation")
    injected.sqlite_errorcode = sqlite3.SQLITE_IOERR

    class Probe:
        def __init__(self, connection):
            self.connection = connection

        def execute(self, sql, *args):
            normalized = " ".join(sql.split()).upper()
            calls.append(normalized)
            result = self.connection.execute(sql, *args)
            if normalized == "COMMIT":
                assert not self.connection.in_transaction
                raise injected
            return result

        def __getattr__(self, name):
            return getattr(self.connection, name)

    class Store(SqliteCaseLifecycleExecutionStore):
        def _connect(self):
            connection = super()._connect()
            return Probe(connection) if enabled[0] else connection

    acquisition = (
        SpacedSqliteWriteAcquisition(pause_ns=1_000_000)
        if spaced else None
    )
    store = Store(
        database_path=path,
        write_acquisition=acquisition,
        write_observer=observations.append,
    )
    if operation == "transition":
        assert store.execute(request=opening().request) == opening()
        expected = completion()
    else:
        expected = opening()

    observations.clear()
    enabled[0] = True
    with pytest.raises(sqlite3.OperationalError) as caught:
        store.execute(
            request=expected.request,
            write_deadline_ns=perf_counter_ns() + 5_000_000_000,
        )
    enabled[0] = False

    assert caught.value is injected
    assert calls.count("BEGIN IMMEDIATE") == 1
    assert calls.count("COMMIT") == 1
    assert "ROLLBACK" not in calls
    assert len(observations) == 1
    assert observations[0].failed
    assert not observations[0].committed
    assert observations[0].rollback_ns is None

    reopened = SqliteCaseLifecycleExecutionStore(
        database_path=path, write_acquisition=acquisition,
    )
    assert reopened.recover(request=expected.request) == expected
    assert reopened.execute(
        request=expected.request,
        write_deadline_ns=perf_counter_ns() + 5_000_000_000,
    ) == expected
    assert reopened.read(case_id="CASE-1") == expected.state
    history = reopened.read_transitions(case_id="CASE-1")
    assert len(history) == expected.state.revision

    # Advance the case using a different operation identity.
    if operation == "opening":
        later_request = completion().request
    else:
        later_request = CaseTransitionRequest(
            transition_id="T-3",
            case_id="CASE-1",
            expected_revision=2,
            to_phase=Phase.AWAITING_EXPERT_DECISION,
        )
    later = reopened.execute(request=later_request)
    assert later.state.revision == expected.state.revision + 1

    # Recovery must return the historical result, not the latest snapshot.
    assert reopened.recover(request=expected.request) == expected
    assert reopened.execute(request=expected.request) == expected
    assert reopened.read(case_id="CASE-1") == later.state
    later_history = reopened.read_transitions(case_id="CASE-1")
    assert len(later_history) == later.state.revision
    assert later_history[:len(history)] == history

    changed = (
        replace(expected.request, scope="OTHER-STORE")
        if operation == "opening"
        else replace(expected.request, expected_revision=7)
    )
    for method in (reopened.recover, reopened.execute):
        with pytest.raises(CaseLifecycleRequestConflict):
            method(request=changed)

    assert reopened.read(case_id="CASE-1") == later.state
    assert reopened.read_transitions(case_id="CASE-1") == later_history

    connection = sqlite3.connect(path)
    try:
        assert connection.execute(
            """SELECT COUNT(*) FROM case_lifecycle_completions
            WHERE transition_id=?""",
            (expected.request.transition_id,),
        ).fetchone()[0] == 1
        assert connection.execute(
            "SELECT COUNT(*) FROM case_lifecycle_completions"
        ).fetchone()[0] == later.state.revision
    finally:
        connection.close()
