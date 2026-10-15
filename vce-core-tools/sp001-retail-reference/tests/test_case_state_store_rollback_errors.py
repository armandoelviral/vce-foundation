import sqlite3

import pytest

from test_sqlite_case_authoritative_state_store import (
    make_state, make_transition,
)
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase as Phase
from sp001.services.sqlite_case_authoritative_state_store import (
    SqliteCaseAuthoritativeStateStore,
)


def operation(adapter, kind):
    if kind == "create":
        return adapter.create(
            state=make_state(), transition=make_transition(),
        )
    return adapter.compare_and_swap(
        expected_revision=1,
        next_state=make_state(
            phase=Phase.RECOMMENDATION_AVAILABLE, revision=2,
        ),
        transition=make_transition(
            revision=2, from_phase=Phase.CASE_OPENED,
            to_phase=Phase.RECOMMENDATION_AVAILABLE,
        ),
    )


@pytest.mark.parametrize("kind", ["create", "compare_and_swap"])
def test_failed_begin_preserves_sqlite_busy_and_changes_nothing(tmp_path, kind):
    path = tmp_path / "case.sqlite3"
    statements = []
    connections = []

    class ImmediateFailureStore(SqliteCaseAuthoritativeStateStore):
        def _connect(self):
            connection = super()._connect()
            # Test-only timeout: exercise real contention without a five-second wait.
            connection.execute("PRAGMA busy_timeout=0")
            connection.set_trace_callback(statements.append)
            connections.append(connection)
            return connection

    adapter = ImmediateFailureStore(database_path=path)
    if kind == "compare_and_swap":
        assert adapter.create(
            state=make_state(), transition=make_transition(),
        )
    before_state = adapter.read(case_id="CASE-001")
    before_history = adapter.read_transitions(case_id="CASE-001")
    statements.clear()
    connections.clear()

    blocker = sqlite3.connect(path, timeout=0)
    try:
        blocker.execute("BEGIN IMMEDIATE")
        with pytest.raises(sqlite3.OperationalError) as caught:
            operation(adapter, kind)
        assert caught.value.sqlite_errorcode == sqlite3.SQLITE_BUSY
        assert "no transaction is active" not in str(caught.value)
        assert not any(
            statement.strip().upper() == "ROLLBACK"
            for statement in statements
        )
        assert len(connections) == 1
        with pytest.raises(sqlite3.ProgrammingError):
            connections[0].execute("SELECT 1")
    finally:
        blocker.rollback()
        blocker.close()

    assert adapter.read(case_id="CASE-001") == before_state
    assert adapter.read_transitions(case_id="CASE-001") == before_history
    # Releasing contention restores the original operation's ability to succeed.
    assert operation(adapter, kind)


@pytest.mark.parametrize("kind", ["create", "compare_and_swap"])
def test_engine_rollback_is_not_replaced_by_invalid_second_rollback(tmp_path, kind):
    path = tmp_path / "case.sqlite3"
    adapter = SqliteCaseAuthoritativeStateStore(database_path=path)
    if kind == "compare_and_swap":
        assert adapter.create(
            state=make_state(), transition=make_transition(),
        )
    before_state = adapter.read(case_id="CASE-001")
    before_history = adapter.read_transitions(case_id="CASE-001")

    with sqlite3.connect(path) as connection:
        connection.execute("""
            CREATE TRIGGER force_engine_rollback
            BEFORE INSERT ON case_lifecycle_transitions
            BEGIN
                SELECT RAISE(ROLLBACK, 'injected engine rollback');
            END
        """)

    # Existing IntegrityError policy remains False; no new OperationalError.
    assert operation(adapter, kind) is False
    assert adapter.read(case_id="CASE-001") == before_state
    assert adapter.read_transitions(case_id="CASE-001") == before_history
