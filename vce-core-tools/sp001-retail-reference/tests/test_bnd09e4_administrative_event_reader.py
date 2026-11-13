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


def record():
    return GrantAdministrationRecord(
        event_id="EVENT-E4-1",
        actor=AuthenticatedPrincipal(
            "issuer-A", "administrator-1"
        ),
        action=Action.GRANT,
        grant=CaseAccessGrant(
            "GRANT-E4-1",
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


def populated_store(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)
    command = record()
    assert store.apply(record=command) is True
    return path, store, command


def test_reads_exact_persisted_event(tmp_path):
    _, store, command = populated_store(tmp_path)

    assert store.read_administration_event(
        event_id=command.event_id
    ) == command

    assert store.read_audit() == (command,)


def test_missing_event_returns_none(tmp_path):
    _, store, command = populated_store(tmp_path)

    assert store.read_administration_event(
        event_id="UNKNOWN-EVENT"
    ) is None

    assert store.read_audit() == (command,)


def test_event_survives_reopen(tmp_path):
    path, _, command = populated_store(tmp_path)
    reopened = SqliteCaseAccessGrants(database_path=path)

    assert reopened.read_administration_event(
        event_id=command.event_id
    ) == command


@pytest.mark.parametrize(
    "invalid, error",
    [
        (None, TypeError),
        (42, TypeError),
        ("", ValueError),
        ("   ", ValueError),
    ],
)
def test_rejects_invalid_event_id(tmp_path, invalid, error):
    store = SqliteCaseAccessGrants(
        database_path=tmp_path / "grants.sqlite3"
    )

    with pytest.raises(error):
        store.read_administration_event(event_id=invalid)


@pytest.mark.parametrize(
    "mutation",
    [
        "event_column_mismatch",
        "grant_column_mismatch",
        "malformed_json",
        "invalid_structure",
        "noncanonical_json",
    ],
)
def test_rejects_invalid_persisted_evidence(tmp_path, mutation):
    path, store, command = populated_store(tmp_path)

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
        event_id, grant_id, stored = row

        if mutation == "event_column_mismatch":
            event_id = "DIFFERENT-EVENT"
        elif mutation == "grant_column_mismatch":
            grant_id = "DIFFERENT-GRANT"
        elif mutation == "malformed_json":
            stored = "{invalid-json"
        elif mutation == "invalid_structure":
            stored = json.dumps({"event_id": command.event_id})
        elif mutation == "noncanonical_json":
            stored = json.dumps(json.loads(stored), indent=2)

        connection.execute(
            """
            UPDATE case_access_grant_audit
            SET event_id=?, grant_id=?, record=?
            WHERE event_id=?
            """,
            (event_id, grant_id, stored, command.event_id),
        )

    lookup_id = (
        "DIFFERENT-EVENT"
        if mutation == "event_column_mismatch"
        else command.event_id
    )

    with pytest.raises((ValueError, TypeError, KeyError)):
        store.read_administration_event(event_id=lookup_id)


def test_storage_failure_does_not_become_absence(tmp_path):
    path, store, command = populated_store(tmp_path)

    with sqlite3.connect(path) as connection:
        connection.execute(
            "DROP TABLE case_access_grant_audit"
        )

    with pytest.raises(sqlite3.Error):
        store.read_administration_event(
            event_id=command.event_id
        )


def test_rejects_duplicate_json_keys(tmp_path):
    path, store, command = populated_store(tmp_path)

    with sqlite3.connect(path) as connection:
        row = connection.execute(
            """
            SELECT record
            FROM case_access_grant_audit
            WHERE event_id=?
            """,
            (command.event_id,),
        ).fetchone()

        assert row is not None
        stored = row[0]

        duplicated = stored.replace(
            '"event_id":"EVENT-E4-1"',
            '"event_id":"FORGED-EVENT","event_id":"EVENT-E4-1"',
            1,
        )

        assert duplicated != stored

        connection.execute(
            """
            UPDATE case_access_grant_audit
            SET record=?
            WHERE event_id=?
            """,
            (duplicated, command.event_id),
        )

    with pytest.raises(ValueError):
        store.read_administration_event(
            event_id=command.event_id
        )


@pytest.mark.parametrize(
    "field, invalid",
    [
        ("recorded_at", True),
        ("recorded_at", -1),
        ("recorded_at", "100"),
        ("event_id", 123),
        ("action", "UNKNOWN_ACTION"),
    ],
)
def test_rejects_invalid_persisted_field_types(
    tmp_path, field, invalid
):
    path, store, command = populated_store(tmp_path)

    with sqlite3.connect(path) as connection:
        row = connection.execute(
            """
            SELECT record
            FROM case_access_grant_audit
            WHERE event_id=?
            """,
            (command.event_id,),
        ).fetchone()

        assert row is not None
        document = json.loads(row[0])
        document[field] = invalid

        connection.execute(
            """
            UPDATE case_access_grant_audit
            SET record=?
            WHERE event_id=?
            """,
            (
                json.dumps(
                    document,
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=True,
                ),
                command.event_id,
            ),
        )

    with pytest.raises((ValueError, TypeError)):
        store.read_administration_event(
            event_id=command.event_id
        )
