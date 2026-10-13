from dataclasses import replace
import sqlite3

import pytest

from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_context import CaseAccessPermission, CaseAccessOperation
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationRecord, GrantAdministrationAction as Action,
)
from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants
from sp001.services.case_access_grant_administration import administer_case_access_grant


PRINCIPAL = AuthenticatedPrincipal("issuer-A", "subscriber-1")
PERMISSION = CaseAccessPermission("CASE-001", CaseAccessOperation.READ_STATE)


def record():
    return GrantAdministrationRecord(
        event_id="EVENT-1",
        actor=AuthenticatedPrincipal("issuer-A", "administrator-1"),
        action=Action.GRANT,
        grant=CaseAccessGrant("GRANT-1", PRINCIPAL, PERMISSION, 100, 200),
        recorded_at=100,
    )


def permitted(store, at_time=150):
    return store.permits(
        principal=PRINCIPAL, permission=PERMISSION, at_time=at_time
    )


def test_grant_and_audit_survive_reopen(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)
    command = record()
    assert store.apply(record=command)
    reopened = SqliteCaseAccessGrants(database_path=path)
    assert permitted(reopened)
    assert reopened.read_audit() == (command,)


def test_exact_event_replay_is_idempotent(tmp_path):
    store = SqliteCaseAccessGrants(database_path=tmp_path / "grants.sqlite3")
    command = record()
    assert store.apply(record=command)
    assert store.apply(record=command)
    assert store.read_audit() == (command,)


@pytest.mark.parametrize("kind", ["event", "grant"])
def test_conflicts_do_not_mutate_or_append_audit(tmp_path, kind):
    store = SqliteCaseAccessGrants(database_path=tmp_path / "grants.sqlite3")
    original = record()
    store.apply(record=original)
    if kind == "event":
        conflicting = replace(original, recorded_at=101)
    else:
        conflicting = replace(
            original, event_id="EVENT-2",
            grant=replace(original.grant, expires_at=300),
        )
    with pytest.raises(ValueError):
        store.apply(record=conflicting)
    assert store.read_audit() == (original,)
    assert not permitted(store, at_time=250)


def test_revocation_persists_and_cannot_be_undone_by_replay(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)
    original = record()
    store.apply(record=original)
    revoked = replace(
        original, event_id="EVENT-2", action=Action.REVOKE, recorded_at=160,
    )
    assert store.apply(record=revoked)
    assert store.apply(record=revoked)
    assert store.apply(record=original)
    reopened = SqliteCaseAccessGrants(database_path=path)
    assert not permitted(reopened, at_time=150)
    assert reopened.read_audit() == (original, revoked)
    with pytest.raises(ValueError, match="cannot be reactivated"):
        reopened.apply(record=replace(original, event_id="EVENT-3"))


def test_unknown_revocation_returns_false_without_audit(tmp_path):
    store = SqliteCaseAccessGrants(database_path=tmp_path / "grants.sqlite3")
    assert not store.apply(record=replace(record(), action=Action.REVOKE))
    assert store.read_audit() == ()


def test_other_active_grant_can_still_permit_access(tmp_path):
    store = SqliteCaseAccessGrants(database_path=tmp_path / "grants.sqlite3")
    first = record()
    second = replace(
        first, event_id="EVENT-2", grant=replace(first.grant, grant_id="GRANT-2"),
    )
    store.apply(record=first)
    store.apply(record=second)
    store.apply(record=replace(
        first, event_id="EVENT-3", action=Action.REVOKE, recorded_at=160,
    ))
    assert permitted(store)


@pytest.mark.parametrize("action", [Action.GRANT, Action.REVOKE])
def test_audit_failure_rolls_back_mutation(tmp_path, action):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)
    original = record()
    if action is Action.REVOKE:
        store.apply(record=original)
    with sqlite3.connect(path) as connection:
        connection.execute("""
            CREATE TRIGGER reject_audit BEFORE INSERT ON case_access_grant_audit
            BEGIN SELECT RAISE(ABORT, 'injected audit failure'); END
        """)
    command = replace(original, event_id="FAIL", action=action)
    with pytest.raises(sqlite3.IntegrityError):
        store.apply(record=command)
    assert permitted(store) is (action is Action.REVOKE)
    assert store.read_audit() == (
        (original,) if action is Action.REVOKE else ()
    )


def test_denied_administration_does_not_persist(tmp_path):
    store = SqliteCaseAccessGrants(database_path=tmp_path / "grants.sqlite3")

    class Policy:
        def may_administer(self, *, actor, action, grant):
            return False

    with pytest.raises(PermissionError):
        administer_case_access_grant(store=store, policy=Policy(), record=record())
    assert not permitted(store)
    assert store.read_audit() == ()


@pytest.mark.parametrize("at_time,expected", [
    (99, False), (100, True), (199, True), (200, False),
])
def test_permission_validity_boundaries(tmp_path, at_time, expected):
    store = SqliteCaseAccessGrants(database_path=tmp_path / "grants.sqlite3")
    store.apply(record=record())
    assert permitted(store, at_time) is expected
