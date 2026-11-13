from dataclasses import replace
import json
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
        event_id="EVENT-E3-1",
        actor=AuthenticatedPrincipal(
            "issuer-A", "administrator-1"
        ),
        action=Action.GRANT,
        grant=CaseAccessGrant(
            "GRANT-E3-1",
            AuthenticatedPrincipal(
                "issuer-A", "subscriber-1"
            ),
            CaseAccessPermission(
                "CASE-001",
                CaseAccessOperation.READ_STATE,
            ),
            100,
            200,
        ),
        recorded_at=100,
    )


def corrupt_audit(tmp_path, mutation):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)
    command = make_record()

    assert store.apply(record=command) is True

    with sqlite3.connect(path) as connection:
        row = connection.execute(
            """
            SELECT event_id, grant_id, record
            FROM case_access_grant_audit
            WHERE event_id=?
            """,
            (command.event_id,),
        ).fetchone()

        assert row is not None
        event_id, grant_id, stored = mutation(*row)

        connection.execute(
            """
            UPDATE case_access_grant_audit
            SET event_id=?, grant_id=?, record=?
            WHERE event_id=?
            """,
            (event_id, grant_id, stored, command.event_id),
        )

    return SqliteCaseAccessGrants(database_path=path), command


def test_column_event_id_mismatch_is_currently_accepted(tmp_path):
    store, command = corrupt_audit(
        tmp_path,
        lambda event_id, grant_id, stored: (
            "DIFFERENT-EVENT", grant_id, stored
        ),
    )

    assert store.read_audit() == (command,)


def test_column_grant_id_mismatch_is_currently_accepted(tmp_path):
    store, command = corrupt_audit(
        tmp_path,
        lambda event_id, grant_id, stored: (
            event_id, "DIFFERENT-GRANT", stored
        ),
    )

    assert store.read_audit() == (command,)


def test_malformed_json_is_rejected(tmp_path):
    store, _ = corrupt_audit(
        tmp_path,
        lambda event_id, grant_id, stored: (
            event_id, grant_id, "{invalid-json"
        ),
    )

    with pytest.raises(json.JSONDecodeError):
        store.read_audit()


def test_invalid_record_structure_is_rejected(tmp_path):
    store, _ = corrupt_audit(
        tmp_path,
        lambda event_id, grant_id, stored: (
            event_id, grant_id, json.dumps({"event_id": event_id})
        ),
    )

    with pytest.raises((KeyError, TypeError, ValueError)):
        store.read_audit()


def test_noncanonical_json_is_currently_accepted(tmp_path):
    def mutation(event_id, grant_id, stored):
        value = json.loads(stored)
        return (
            event_id,
            grant_id,
            json.dumps(value, indent=2),
        )

    store, command = corrupt_audit(tmp_path, mutation)

    assert store.read_audit() == (command,)
