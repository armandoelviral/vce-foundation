import sqlite3

import pytest

from test_case_access_issuance_completion import components
from sp001.infrastructure.sqlite_case_access_issuance_completions import (
    SqliteCaseAccessIssuanceCompletions,
)
from sp001.services.prepared_case_access_completion import (
    PreparedCaseAccessCompleter,
)


def measured(components, observer):
    path, _, _, _, _, signer, protector, _ = components
    store = SqliteCaseAccessIssuanceCompletions(
        database_path=path, write_observer=observer,
    )
    return store, PreparedCaseAccessCompleter(
        store=store, signer=signer, protector=protector, clock=lambda: 150,
    )


def test_observer_runs_after_connection_release_and_durable_commit(components):
    path, _, _, _, preparation, _, _, _ = components
    observations = []

    def observe(value):
        with sqlite3.connect(path, timeout=0) as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT status FROM case_access_issuance_completions "
                "WHERE request_id=?", (preparation.request_id,),
            ).fetchone()
            connection.rollback()
        assert row == ("COMPLETED",)
        observations.append(value)

    _, completer = measured(components, observe)
    token = completer.complete(request_id=preparation.request_id)
    assert token is not None
    assert len(observations) == 1
    value = observations[0]
    assert value.operation == "issuance.confirm"
    assert value.committed
    assert not value.failed
    assert value.begin_ns >= 0
    assert value.commit_ns >= 0
    assert value.rollback_ns is None
    assert value.total_ns >= value.begin_ns + value.commit_ns
    assert token.credential not in repr(value)


def test_rejected_confirmation_reports_rollback_and_preserves_state(components):
    preparation = components[4]
    observations = []
    store, completer = measured(components, observations.append)

    def reject():
        raise PermissionError("injected rejection")

    with pytest.raises(PermissionError, match="injected rejection"):
        completer.complete(
            request_id=preparation.request_id, before_commit=reject,
        )
    assert store.read_completed(request_id=preparation.request_id) is None
    assert len(observations) == 1
    value = observations[0]
    assert not value.committed
    assert value.failed
    assert value.commit_ns is None
    assert value.rollback_ns >= 0


def test_observer_failure_does_not_turn_committed_operation_into_error(components):
    calls = []

    def broken_observer(value):
        calls.append(value)
        raise RuntimeError("telemetry unavailable")

    store, completer = measured(components, broken_observer)
    preparation = components[4]
    token = completer.complete(request_id=preparation.request_id)
    assert token is not None
    assert store.read_completed(request_id=preparation.request_id) is not None
    assert len(calls) == 1
    assert calls[0].committed


def test_invalid_observer_creates_no_database(tmp_path):
    path = tmp_path / "must-not-exist.sqlite3"
    with pytest.raises(TypeError, match="observer"):
        SqliteCaseAccessIssuanceCompletions(
            database_path=path, write_observer=123,
        )
    assert not path.exists()
