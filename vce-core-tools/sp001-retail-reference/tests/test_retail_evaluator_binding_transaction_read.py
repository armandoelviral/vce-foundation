import sqlite3

import pytest

from sp001.infrastructure.sqlite_retail_evaluator_bindings import (
    SqliteRetailEvaluatorBindings,
)


def test_reads_with_caller_transaction_without_opening_another_connection(
    tmp_path, monkeypatch,
):
    path = tmp_path / "bindings.sqlite3"
    store = SqliteRetailEvaluatorBindings(database_path=path)
    connection = sqlite3.connect(path, isolation_level=None)
    try:
        connection.execute("BEGIN IMMEDIATE")

        def forbidden():
            raise AssertionError("must use the supplied connection")

        monkeypatch.setattr(store, "_connect", forbidden)
        assert store.read_snapshot_in_transaction(
            connection=connection, binding_id="MISSING",
        ) is None
        assert connection.in_transaction
        assert connection.execute("SELECT 1").fetchone() == (1,)
        connection.execute("ROLLBACK")
    finally:
        connection.close()


def test_requires_an_active_transaction(tmp_path):
    path = tmp_path / "bindings.sqlite3"
    store = SqliteRetailEvaluatorBindings(database_path=path)
    connection = sqlite3.connect(path, isolation_level=None)
    try:
        with pytest.raises(ValueError, match="active transaction"):
            store.read_snapshot_in_transaction(
                connection=connection, binding_id="BINDING-1",
            )
        assert not connection.in_transaction
    finally:
        connection.close()


@pytest.mark.parametrize("binding_id", ["", "   ", None, 1])
def test_rejects_invalid_identity_without_ending_transaction(
    tmp_path, binding_id,
):
    path = tmp_path / "bindings.sqlite3"
    store = SqliteRetailEvaluatorBindings(database_path=path)
    connection = sqlite3.connect(path, isolation_level=None)
    try:
        connection.execute("BEGIN")
        with pytest.raises((TypeError, ValueError)):
            store.read_snapshot_in_transaction(
                connection=connection, binding_id=binding_id,
            )
        assert connection.in_transaction
        connection.execute("ROLLBACK")
    finally:
        connection.close()


def test_missing_schema_is_a_failure_not_an_absent_binding(tmp_path):
    store = SqliteRetailEvaluatorBindings(
        database_path=tmp_path / "bindings.sqlite3",
    )
    connection = sqlite3.connect(":memory:", isolation_level=None)
    try:
        connection.execute("BEGIN")
        with pytest.raises(sqlite3.OperationalError):
            store.read_snapshot_in_transaction(
                connection=connection, binding_id="BINDING-1",
            )
        assert connection.in_transaction
        connection.execute("ROLLBACK")
    finally:
        connection.close()
