import sqlite3

import pytest

from test_case_lifecycle_completion import opening, completion
from sp001.infrastructure.sqlite_case_lifecycle_execution import (
    SqliteCaseLifecycleExecutionStore,
)
from sp001.infrastructure.sqlite_write_acquisition import (
    SpacedSqliteWriteAcquisition,
)
from sp001.runtime.scientific_product_runtime import ScientificProductRuntime


@pytest.mark.parametrize("operation", ["opening", "transition"])
@pytest.mark.parametrize("spaced", [False, True])
def test_runtime_recovers_after_commit_confirmation_is_lost(
    tmp_path, operation, spaced,
):
    path = tmp_path / "case.sqlite3"
    enabled = [False]
    calls = []
    injected = sqlite3.OperationalError("controlled post-commit confirmation loss")
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

    option = (
        SpacedSqliteWriteAcquisition(pause_ns=1_000_000)
        if spaced else None
    )
    store = Store(database_path=path, write_acquisition=option)
    runtime = ScientificProductRuntime(
        case_authoritative_state_store=store,
        case_lifecycle_execution_store=store,
        case_write_budget_ns=5_000_000_000,
    )
    if operation == "transition":
        assert runtime.execute_case_lifecycle(
            request=opening().request,
        ) == opening()
        expected = completion()
    else:
        expected = opening()

    enabled[0] = True
    with pytest.raises(sqlite3.OperationalError) as caught:
        runtime.execute_case_lifecycle(request=expected.request)
    enabled[0] = False

    assert caught.value is injected
    assert calls.count("BEGIN IMMEDIATE") == 1
    assert calls.count("COMMIT") == 1
    assert "ROLLBACK" not in calls

    reopened = SqliteCaseLifecycleExecutionStore(
        database_path=path, write_acquisition=option,
    )
    recovered_runtime = ScientificProductRuntime(
        case_authoritative_state_store=reopened,
        case_lifecycle_execution_store=reopened,
        case_write_budget_ns=5_000_000_000,
    )
    assert recovered_runtime.recover_case_lifecycle(
        request=expected.request,
    ) == expected
    assert recovered_runtime.execute_case_lifecycle(
        request=expected.request,
    ) == expected
    assert recovered_runtime.read_case_authoritative_state(
        case_id=expected.request.case_id,
    ) == expected.state

    history = reopened.read_transitions(case_id=expected.request.case_id)
    assert len(history) == expected.state.revision
    assert history[-1] == expected.transition

    connection = sqlite3.connect(path)
    try:
        assert connection.execute(
            """SELECT COUNT(*) FROM case_lifecycle_completions
            WHERE transition_id=?""",
            (expected.request.transition_id,),
        ).fetchone()[0] == 1
        assert connection.execute(
            "SELECT COUNT(*) FROM case_lifecycle_completions"
        ).fetchone()[0] == expected.state.revision
    finally:
        connection.close()
