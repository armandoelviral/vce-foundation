import sqlite3
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from threading import Barrier

import pytest

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_process_actor import ActorType, RetailProcessActor
from sp001.contracts.retail_process_role import RetailProcessRole
from sp001.contracts.retail_evaluator_binding import (
    RetailEvaluatorBinding, RetailEvaluatorBindingSnapshot,
)
from sp001.contracts.retail_evaluator_binding_change import (
    RetailEvaluatorBindingChange,
)
from sp001.infrastructure.sqlite_retail_evaluator_bindings import (
    SqliteRetailEvaluatorBindings, RetailEvaluatorBindingConflict,
)


def change():
    actor = RetailProcessActor(
        "ACTOR", "CUSTOMER", ActorType.HUMAN, "ORG",
        RetailProcessRole("ROLE", "CUSTOMER", "VM reviewer"),
    )
    binding = RetailEvaluatorBinding(
        "BINDING", 1, AuthenticatedPrincipal("ISSUER", "SUBJECT"),
        actor, "CASE", 100, 200,
    )
    return RetailEvaluatorBindingChange(
        "EVENT-1", RetailEvaluatorBindingSnapshot(binding, False),
        AuthenticatedPrincipal("ADMIN-ISSUER", "ADMIN"), 100,
    )


def successor(previous, *, event_id, revoked=False, expires_at=None):
    binding = replace(
        previous.snapshot.binding,
        revision=previous.snapshot.binding.revision + 1,
    )
    if expires_at is not None:
        binding = replace(binding, expires_at=expires_at)
    return replace(
        previous, event_id=event_id,
        snapshot=RetailEvaluatorBindingSnapshot(binding, revoked),
        recorded_at=previous.recorded_at + 1,
    )


def test_reopen_history_idempotence_and_terminal_revocation(tmp_path):
    path = tmp_path / "bindings.sqlite3"
    store = SqliteRetailEvaluatorBindings(database_path=path)
    first = change()
    revised = successor(first, event_id="EVENT-2", expires_at=300)
    revoked = successor(revised, event_id="EVENT-3", revoked=True)
    for event in (first, revised, revoked):
        assert store.apply(change=event)
        assert store.apply(change=event)

    reopened = SqliteRetailEvaluatorBindings(database_path=path)
    assert reopened.read_history(binding_id="BINDING") == (
        first, revised, revoked,
    )
    assert reopened.read_snapshot(binding_id="BINDING") == revoked.snapshot
    assert reopened.read_snapshot(binding_id="ABSENT") is None
    with pytest.raises(RetailEvaluatorBindingConflict):
        reopened.apply(change=successor(revoked, event_id="EVENT-4"))
    assert reopened.read_snapshot(binding_id="BINDING") == revoked.snapshot


@pytest.mark.parametrize("kind", ["event", "revision", "association"])
def test_conflict_preserves_history(tmp_path, kind):
    store = SqliteRetailEvaluatorBindings(
        database_path=tmp_path / "bindings.sqlite3"
    )
    first = change()
    store.apply(change=first)
    candidate = successor(first, event_id="EVENT-2")
    if kind == "event":
        candidate = replace(candidate, event_id=first.event_id)
    elif kind == "revision":
        candidate = replace(candidate, snapshot=replace(
            candidate.snapshot,
            binding=replace(candidate.snapshot.binding, revision=3),
        ))
    else:
        candidate = replace(candidate, snapshot=replace(
            candidate.snapshot,
            binding=replace(candidate.snapshot.binding, case_id="OTHER"),
        ))
    with pytest.raises(RetailEvaluatorBindingConflict):
        store.apply(change=candidate)
    assert store.read_history(binding_id="BINDING") == (first,)


def test_revocation_cannot_also_change_validity(tmp_path):
    store = SqliteRetailEvaluatorBindings(
        database_path=tmp_path / "bindings.sqlite3"
    )
    first = change()
    store.apply(change=first)
    with pytest.raises(RetailEvaluatorBindingConflict):
        store.apply(change=successor(
            first, event_id="REVOKE", revoked=True, expires_at=300,
        ))
    assert store.read_snapshot(binding_id="BINDING") == first.snapshot


@pytest.mark.parametrize("contradictory", [False, True])
def test_two_connections_preserve_one_successor(tmp_path, contradictory):
    path = tmp_path / "bindings.sqlite3"
    stores = [SqliteRetailEvaluatorBindings(database_path=path) for _ in range(2)]
    first = change()
    stores[0].apply(change=first)
    second = successor(first, event_id="EVENT-2", expires_at=300)
    alternative = (
        successor(first, event_id="OTHER-EVENT", expires_at=400)
        if contradictory else second
    )
    events = (second, alternative)
    barrier = Barrier(2)

    def attempt(index):
        barrier.wait(timeout=5)
        try:
            stores[index].apply(change=events[index])
            return events[index]
        except RetailEvaluatorBindingConflict:
            return None

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(attempt, range(2)))
    confirmed = [result for result in results if result is not None]
    assert len(confirmed) == (1 if contradictory else 2)
    history = stores[0].read_history(binding_id="BINDING")
    assert len(history) == 2
    assert history[0] == first
    assert history[1] == confirmed[0]


def test_detects_metadata_content_inconsistency(tmp_path):
    path = tmp_path / "bindings.sqlite3"
    store = SqliteRetailEvaluatorBindings(database_path=path)
    store.apply(change=change())
    with sqlite3.connect(path) as connection:
        connection.execute(
            "UPDATE retail_evaluator_binding_history SET revision='9'"
        )
    with pytest.raises(ValueError, match="metadata mismatch"):
        store.read_snapshot(binding_id="BINDING")


def test_backend_failure_is_not_absence(tmp_path):
    path = tmp_path / "bindings.sqlite3"
    store = SqliteRetailEvaluatorBindings(database_path=path)
    with sqlite3.connect(path) as connection:
        connection.execute("DROP TABLE retail_evaluator_binding_history")
    with pytest.raises(sqlite3.OperationalError):
        store.read_snapshot(binding_id="ABSENT")
