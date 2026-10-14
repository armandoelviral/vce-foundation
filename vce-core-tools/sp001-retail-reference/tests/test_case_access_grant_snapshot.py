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


def record():
    return GrantAdministrationRecord(
        event_id="CREATE-1",
        actor=AuthenticatedPrincipal("issuer-A", "administrator-1"),
        action=Action.GRANT,
        grant=CaseAccessGrant(
            "GRANT-1", AuthenticatedPrincipal("issuer-A", "subscriber-1"),
            CaseAccessPermission("CASE-001", CaseAccessOperation.READ_STATE),
            100, 200,
        ),
        recorded_at=100,
    )


def test_revision_and_revocation_survive_reopen(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)
    command = record()
    store.apply(record=command)
    first = store.read_grant_snapshot(grant_id="GRANT-1")
    assert first.grant == command.grant
    assert first.revision == 1
    assert first.revoked is False

    store.apply(record=replace(
        command, event_id="REVOKE-1", action=Action.REVOKE, recorded_at=150,
    ))
    reopened = SqliteCaseAccessGrants(database_path=path)
    second = reopened.read_grant_snapshot(grant_id="GRANT-1")
    assert second.grant == first.grant
    assert second.revision == 2
    assert second.revoked is True


def test_exact_replays_do_not_change_revision(tmp_path):
    store = SqliteCaseAccessGrants(database_path=tmp_path / "grants.sqlite3")
    command = record()
    store.apply(record=command)
    before = store.read_grant_snapshot(grant_id="GRANT-1")
    store.apply(record=command)
    assert store.read_grant_snapshot(grant_id="GRANT-1") == before


def test_conflict_does_not_change_revision(tmp_path):
    store = SqliteCaseAccessGrants(database_path=tmp_path / "grants.sqlite3")
    command = record()
    store.apply(record=command)
    with pytest.raises(ValueError):
        store.apply(record=replace(command, recorded_at=101))
    assert store.read_grant_snapshot(grant_id="GRANT-1").revision == 1


def test_missing_snapshot_is_explicit(tmp_path):
    store = SqliteCaseAccessGrants(database_path=tmp_path / "grants.sqlite3")
    assert store.read_grant_snapshot(grant_id="MISSING") is None


def test_revision_is_per_grant_not_global_event_count(tmp_path):
    store = SqliteCaseAccessGrants(database_path=tmp_path / "grants.sqlite3")
    command = record()
    store.apply(record=command)
    store.apply(record=replace(
        command, event_id="CREATE-2",
        grant=replace(command.grant, grant_id="GRANT-2"),
    ))
    assert store.read_grant_snapshot(grant_id="GRANT-1").revision == 1
    assert store.read_grant_snapshot(grant_id="GRANT-2").revision == 1


def test_grant_without_audit_is_rejected_as_inconsistent(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)
    store.apply(record=record())
    with sqlite3.connect(path) as connection:
        connection.execute("DELETE FROM case_access_grant_audit")
    with pytest.raises(ValueError, match="inconsistent"):
        store.read_grant_snapshot(grant_id="GRANT-1")
