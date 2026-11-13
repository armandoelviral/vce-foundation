from dataclasses import replace

import pytest

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


def record():
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


def snapshot(store):
    return store.read_grant_snapshot(grant_id="GRANT-1")


def assert_unchanged(store, before_state, before_audit):
    assert snapshot(store) == before_state
    assert store.read_audit() == before_audit


def test_grant_active_conflicting_definition_rejected(tmp_path):
    store = SqliteCaseAccessGrants(
        database_path=tmp_path / "grants.sqlite3"
    )
    first = record()
    assert store.apply(record=first) is True

    before_state = snapshot(store)
    before_audit = store.read_audit()

    conflict = replace(
        first,
        event_id="CREATE-2",
        grant=replace(first.grant, expires_at=300),
    )

    with pytest.raises(ValueError, match="grant_id conflicts"):
        store.apply(record=conflict)

    assert_unchanged(store, before_state, before_audit)


def test_grant_revoked_cannot_reactivate(tmp_path):
    store = SqliteCaseAccessGrants(
        database_path=tmp_path / "grants.sqlite3"
    )
    first = record()
    revoked = replace(
        first,
        event_id="REVOKE-1",
        action=Action.REVOKE,
    )

    assert store.apply(record=first) is True
    assert store.apply(record=revoked) is True

    before_state = snapshot(store)
    before_audit = store.read_audit()

    attempt = replace(first, event_id="CREATE-2")

    with pytest.raises(ValueError, match="cannot be reactivated"):
        store.apply(record=attempt)

    assert_unchanged(store, before_state, before_audit)
    assert snapshot(store).revoked is True


def test_grant_revoked_conflicting_definition_rejected(tmp_path):
    store = SqliteCaseAccessGrants(
        database_path=tmp_path / "grants.sqlite3"
    )
    first = record()
    revoked = replace(
        first,
        event_id="REVOKE-1",
        action=Action.REVOKE,
    )

    assert store.apply(record=first) is True
    assert store.apply(record=revoked) is True

    before_state = snapshot(store)
    before_audit = store.read_audit()

    conflict = replace(
        first,
        event_id="CREATE-2",
        grant=replace(first.grant, expires_at=300),
    )

    with pytest.raises(ValueError, match="grant_id conflicts"):
        store.apply(record=conflict)

    assert_unchanged(store, before_state, before_audit)


@pytest.mark.parametrize("already_revoked", [False, True])
def test_revoke_conflicting_definition_rejected(
    tmp_path, already_revoked
):
    store = SqliteCaseAccessGrants(
        database_path=tmp_path / "grants.sqlite3"
    )
    first = record()
    assert store.apply(record=first) is True

    if already_revoked:
        assert store.apply(
            record=replace(
                first,
                event_id="REVOKE-1",
                action=Action.REVOKE,
            )
        ) is True

    before_state = snapshot(store)
    before_audit = store.read_audit()

    conflict = replace(
        first,
        event_id="REVOKE-2",
        action=Action.REVOKE,
        grant=replace(first.grant, expires_at=300),
    )

    with pytest.raises(ValueError, match="grant_id conflicts"):
        store.apply(record=conflict)

    assert_unchanged(store, before_state, before_audit)


def test_event_id_conflict_rejected(tmp_path):
    store = SqliteCaseAccessGrants(
        database_path=tmp_path / "grants.sqlite3"
    )
    first = record()
    assert store.apply(record=first) is True

    before_state = snapshot(store)
    before_audit = store.read_audit()

    conflict = replace(first, recorded_at=101)

    with pytest.raises(ValueError, match="event_id conflicts"):
        store.apply(record=conflict)

    assert_unchanged(store, before_state, before_audit)


def test_exact_event_replay_does_not_duplicate(tmp_path):
    store = SqliteCaseAccessGrants(
        database_path=tmp_path / "grants.sqlite3"
    )
    first = record()

    assert store.apply(record=first) is True

    before_state = snapshot(store)
    before_audit = store.read_audit()

    assert store.apply(record=first) is True

    assert_unchanged(store, before_state, before_audit)
    assert store.read_audit() == (first,)
