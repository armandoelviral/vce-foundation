import sqlite3

import pytest

from test_sqlite_case_authoritative_state_store import make_state, make_transition
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase as Phase
from sp001.services.sqlite_case_authoritative_state_store import (
    SqliteCaseAuthoritativeStateStore,
)


def advance(adapter, *, expected_revision=1):
    return adapter.compare_and_swap(
        expected_revision=expected_revision,
        next_state=make_state(
            phase=Phase.RECOMMENDATION_AVAILABLE, revision=2,
        ),
        transition=make_transition(
            revision=2, from_phase=Phase.CASE_OPENED,
            to_phase=Phase.RECOMMENDATION_AVAILABLE,
        ),
    )


def test_committed_create_and_transition_are_visible_before_observation(tmp_path):
    path = tmp_path / "case.sqlite3"
    values = []

    def observe(value):
        with sqlite3.connect(path, timeout=0) as connection:
            connection.execute("BEGIN IMMEDIATE")
            count = connection.execute(
                "SELECT COUNT(*) FROM case_lifecycle_transitions"
            ).fetchone()[0]
            connection.rollback()
        values.append((value, count))

    adapter = SqliteCaseAuthoritativeStateStore(
        database_path=path, write_observer=observe,
    )
    assert values == []
    assert adapter.create(state=make_state(), transition=make_transition())
    assert advance(adapter)
    assert [count for _, count in values] == [1, 2]
    assert [value.operation for value, _ in values] == [
        "case.create", "case.compare_and_swap",
    ]
    for value, _ in values:
        assert value.committed
        assert not value.failed
        assert value.begin_ns >= 0
        assert value.commit_ns >= 0
        assert value.rollback_ns is None
        assert value.total_ns >= value.begin_ns + value.commit_ns
    assert adapter.read(case_id="CASE-001").revision == 2


def test_revision_conflict_reports_rollback_without_commit(tmp_path):
    values = []
    adapter = SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3",
        write_observer=values.append,
    )
    assert adapter.create(state=make_state(), transition=make_transition())
    values.clear()
    assert not advance(adapter, expected_revision=7)
    assert len(values) == 1
    value = values[0]
    assert not value.committed
    assert not value.failed  # False result, no exception escaped.
    assert value.commit_ns is None
    assert value.rollback_ns >= 0
    assert adapter.read(case_id="CASE-001").revision == 1
    assert len(adapter.read_transitions(case_id="CASE-001")) == 1


@pytest.mark.parametrize("operation", ["create", "compare_and_swap"])
def test_failed_begin_is_observed_without_invalid_rollback(tmp_path, operation):
    path = tmp_path / "case.sqlite3"
    values = []

    class ImmediateFailureStore(SqliteCaseAuthoritativeStateStore):
        def _connect(self):
            connection = super()._connect()
            connection.execute("PRAGMA busy_timeout=0")
            return connection

    adapter = ImmediateFailureStore(
        database_path=path, write_observer=values.append,
    )
    if operation == "compare_and_swap":
        assert adapter.create(state=make_state(), transition=make_transition())
    values.clear()
    blocker = sqlite3.connect(path, timeout=0)
    try:
        blocker.execute("BEGIN IMMEDIATE")
        with pytest.raises(sqlite3.OperationalError) as caught:
            if operation == "create":
                adapter.create(state=make_state(), transition=make_transition())
            else:
                advance(adapter)
        assert caught.value.sqlite_errorcode == sqlite3.SQLITE_BUSY
    finally:
        blocker.rollback()
        blocker.close()

    assert len(values) == 1
    value = values[0]
    assert value.operation == "case." + operation
    assert value.failed
    assert not value.committed
    assert value.begin_ns >= 0
    assert value.commit_ns is None
    assert value.rollback_ns is None


def test_observer_exception_does_not_change_persisted_result(tmp_path):
    def broken_observer(value):
        raise RuntimeError("telemetry failure")

    adapter = SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3",
        write_observer=broken_observer,
    )
    assert adapter.create(state=make_state(), transition=make_transition())
    assert advance(adapter)
    assert adapter.read(case_id="CASE-001").revision == 2


def test_invalid_observer_creates_no_database(tmp_path):
    path = tmp_path / "must-not-exist.sqlite3"
    with pytest.raises(TypeError, match="observer"):
        SqliteCaseAuthoritativeStateStore(
            database_path=path, write_observer=123,
        )
    assert not path.exists()
