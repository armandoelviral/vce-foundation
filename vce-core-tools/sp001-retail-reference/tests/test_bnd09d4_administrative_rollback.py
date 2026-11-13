from dataclasses import replace
import sqlite3

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


def make_record():
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


def install_failure_trigger(path):
    with sqlite3.connect(path) as connection:
        connection.execute("""
            CREATE TRIGGER fail_administrative_audit
            BEFORE INSERT ON case_access_grant_audit
            BEGIN
                SELECT RAISE(
                    ABORT,
                    'injected administrative audit failure'
                );
            END
        """)


def test_failed_grant_audit_rolls_back_grant_creation(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)
    first = make_record()

    install_failure_trigger(path)

    with pytest.raises(
        sqlite3.IntegrityError,
        match="injected administrative audit failure",
    ):
        store.apply(record=first)

    reopened = SqliteCaseAccessGrants(database_path=path)

    assert reopened.read_grant_snapshot(grant_id="GRANT-1") is None
    assert reopened.read_audit() == ()


def test_failed_revoke_audit_rolls_back_revocation(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)
    first = make_record()

    assert store.apply(record=first) is True

    before = store.read_grant_snapshot(grant_id="GRANT-1")
    audit_before = store.read_audit()

    install_failure_trigger(path)

    revoke = replace(
        first,
        event_id="REVOKE-1",
        action=Action.REVOKE,
        recorded_at=150,
    )

    with pytest.raises(
        sqlite3.IntegrityError,
        match="injected administrative audit failure",
    ):
        store.apply(record=revoke)

    reopened = SqliteCaseAccessGrants(database_path=path)

    assert reopened.read_grant_snapshot(grant_id="GRANT-1") == before
    assert reopened.read_grant_snapshot(grant_id="GRANT-1").revoked is False
    assert reopened.read_audit() == audit_before
    assert reopened.read_audit() == (first,)
