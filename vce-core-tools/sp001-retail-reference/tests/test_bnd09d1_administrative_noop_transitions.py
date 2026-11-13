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


def make_record():
    return GrantAdministrationRecord(
        event_id="CREATE-1",
        actor=AuthenticatedPrincipal("issuer-A", "administrator-1"),
        action=Action.GRANT,
        grant=CaseAccessGrant(
            "GRANT-1",
            AuthenticatedPrincipal("issuer-A", "subscriber-1"),
            CaseAccessPermission(
                "CASE-001",
                CaseAccessOperation.READ_STATE,
            ),
            100,
            200,
        ),
        recorded_at=100,
    )


def test_new_grant_event_on_active_grant_preserves_state(tmp_path):
    store = SqliteCaseAccessGrants(
        database_path=tmp_path / "grants.sqlite3"
    )
    first = make_record()

    assert store.apply(record=first) is True
    before = store.read_grant_snapshot(grant_id="GRANT-1")
    audit_before = store.read_audit()

    second = replace(
        first,
        event_id="CREATE-2",
        recorded_at=101,
    )

    assert store.apply(record=second) is True

    after = store.read_grant_snapshot(grant_id="GRANT-1")
    audit_after = store.read_audit()

    assert before.revoked is False
    assert after.revoked is False
    assert after.grant == before.grant
    assert after.revision == before.revision + 1

    assert audit_after == audit_before + (second,)
    assert audit_after == (first, second)


def test_new_revoke_event_on_revoked_grant_preserves_state(tmp_path):
    store = SqliteCaseAccessGrants(
        database_path=tmp_path / "grants.sqlite3"
    )
    first = make_record()
    revoke_first = replace(
        first,
        event_id="REVOKE-1",
        action=Action.REVOKE,
        recorded_at=150,
    )
    revoke_second = replace(
        revoke_first,
        event_id="REVOKE-2",
        recorded_at=151,
    )

    assert store.apply(record=first) is True
    assert store.apply(record=revoke_first) is True

    before = store.read_grant_snapshot(grant_id="GRANT-1")
    audit_before = store.read_audit()

    assert store.apply(record=revoke_second) is True

    after = store.read_grant_snapshot(grant_id="GRANT-1")
    audit_after = store.read_audit()

    assert before.revoked is True
    assert after.revoked is True
    assert after.grant == before.grant
    assert after.revision == before.revision + 1

    assert audit_after == audit_before + (revoke_second,)
    assert audit_after == (first, revoke_first, revoke_second)
