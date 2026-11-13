from dataclasses import replace

from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_context import (
    CaseAccessOperation,
    CaseAccessPermission,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action,
    GrantAdministrationRecord,
)
from sp001.infrastructure.sqlite_case_access_grants import (
    SqliteCaseAccessGrants,
)


def make_grant_record():
    return GrantAdministrationRecord(
        event_id="CREATE-1",
        actor=AuthenticatedPrincipal("issuer-A", "administrator-1"),
        action=Action.GRANT,
        grant=CaseAccessGrant(
            "GRANT-1",
            AuthenticatedPrincipal("issuer-A", "subscriber-1"),
            CaseAccessPermission(
                "CASE-001", CaseAccessOperation.READ_STATE
            ),
            100,
            200,
        ),
        recorded_at=100,
    )


def prepare_revoked_store(path):
    store = SqliteCaseAccessGrants(database_path=path)
    grant_event = make_grant_record()
    revoke_event = replace(
        grant_event,
        event_id="REVOKE-1",
        action=Action.REVOKE,
        recorded_at=150,
    )

    assert store.apply(record=grant_event) is True
    assert store.apply(record=revoke_event) is True

    return store, grant_event, revoke_event


def test_grant_replay_after_revocation_does_not_reactivate(tmp_path):
    store, grant_event, revoke_event = prepare_revoked_store(
        tmp_path / "grants.sqlite3"
    )

    before = store.read_grant_snapshot(grant_id="GRANT-1")
    audit_before = store.read_audit()

    assert store.apply(record=grant_event) is True

    after = store.read_grant_snapshot(grant_id="GRANT-1")

    assert before.revoked is True
    assert after == before
    assert after.revision == 2
    assert store.read_audit() == audit_before
    assert audit_before == (grant_event, revoke_event)


def test_reopen_preserves_revocation_and_history(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store, grant_event, revoke_event = prepare_revoked_store(path)

    before = store.read_grant_snapshot(grant_id="GRANT-1")
    audit_before = store.read_audit()

    reopened = SqliteCaseAccessGrants(database_path=path)

    assert reopened.read_grant_snapshot(grant_id="GRANT-1") == before
    assert reopened.read_audit() == audit_before
    assert reopened.read_audit() == (grant_event, revoke_event)
    assert before.revoked is True
    assert before.revision == 2


def test_revoke_replay_after_reopen_does_not_duplicate(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store, grant_event, revoke_event = prepare_revoked_store(path)

    reopened = SqliteCaseAccessGrants(database_path=path)

    before = reopened.read_grant_snapshot(grant_id="GRANT-1")
    audit_before = reopened.read_audit()

    assert reopened.apply(record=revoke_event) is True

    assert reopened.read_grant_snapshot(grant_id="GRANT-1") == before
    assert reopened.read_audit() == audit_before
    assert audit_before == (grant_event, revoke_event)
