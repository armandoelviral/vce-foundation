import json
import sqlite3

import pytest

from sp001.infrastructure.sqlite_case_access_grants import (
    SqliteCaseAccessGrants,
    InvalidPersistedAdministrationEventError,
)


@pytest.mark.parametrize(
    "invalid",
    [
        None,
        123,
    ],
)
def test_invalid_event_id_type_remains_input_error(tmp_path, invalid):
    store = SqliteCaseAccessGrants(
        database_path=tmp_path / "grants.sqlite3"
    )

    with pytest.raises(TypeError):
        store.read_administration_event(event_id=invalid)


def test_empty_event_id_remains_input_error(tmp_path):
    store = SqliteCaseAccessGrants(
        database_path=tmp_path / "grants.sqlite3"
    )

    with pytest.raises(ValueError) as caught:
        store.read_administration_event(event_id="")

    assert type(caught.value) is ValueError


def test_invalid_persisted_structure_has_domain_error(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)

    with sqlite3.connect(path) as connection:
        connection.execute("PRAGMA foreign_keys=OFF")
        connection.execute(
            """
            INSERT INTO case_access_grant_audit
            (event_id, grant_id, record)
            VALUES (?, ?, ?)
            """,
            (
                "EVENT-E5-1",
                "GRANT-E5-1",
                json.dumps({"event_id": "EVENT-E5-1"}),
            ),
        )

    with pytest.raises(
        InvalidPersistedAdministrationEventError
    ):
        store.read_administration_event(event_id="EVENT-E5-1")


def test_storage_failure_remains_sqlite_error(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)

    with sqlite3.connect(path) as connection:
        connection.execute("DROP TABLE case_access_grant_audit")

    with pytest.raises(sqlite3.Error):
        store.read_administration_event(event_id="EVENT-E5-1")


def test_identity_mismatch_has_domain_error(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)

    with sqlite3.connect(path) as connection:
        connection.execute("PRAGMA foreign_keys=OFF")
        connection.execute(
            """
            INSERT INTO case_access_grant_audit
            (event_id, grant_id, record)
            VALUES (?, ?, ?)
            """,
            (
                "EVENT-E5-IDENTITY",
                "GRANT-E5-IDENTITY",
                json.dumps({
                    "event_id": "DIFFERENT-EVENT",
                    "actor": {
                        "issuer": "issuer",
                        "subject": "actor",
                    },
                    "action": "GRANT",
                    "grant": {
                        "grant_id": "GRANT-E5-IDENTITY",
                        "principal": {
                            "issuer": "issuer",
                            "subject": "subject",
                        },
                        "permission": {
                            "case_id": "CASE-001",
                            "operation": "READ_STATE",
                        },
                        "valid_from": 100,
                        "expires_at": 200,
                    },
                    "recorded_at": 100,
                }, sort_keys=True, separators=(",", ":")),
            ),
        )

    with pytest.raises(
        InvalidPersistedAdministrationEventError
    ):
        store.read_administration_event(
            event_id="EVENT-E5-IDENTITY"
        )


def test_noncanonical_record_has_domain_error(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)

    with sqlite3.connect(path) as connection:
        connection.execute("PRAGMA foreign_keys=OFF")
        connection.execute(
            """
            INSERT INTO case_access_grant_audit
            (event_id, grant_id, record)
            VALUES (?, ?, ?)
            """,
            (
                "EVENT-E5-CANONICAL",
                "GRANT-E5-CANONICAL",
                json.dumps({
                    "event_id": "EVENT-E5-CANONICAL",
                    "actor": {
                        "issuer": "issuer",
                        "subject": "actor",
                    },
                    "action": "GRANT",
                    "grant": {
                        "grant_id": "GRANT-E5-CANONICAL",
                        "principal": {
                            "issuer": "issuer",
                            "subject": "subject",
                        },
                        "permission": {
                            "case_id": "CASE-001",
                            "operation": "READ_STATE",
                        },
                        "valid_from": 100,
                        "expires_at": 200,
                    },
                    "recorded_at": 100,
                }, indent=2),
            ),
        )

    with pytest.raises(
        InvalidPersistedAdministrationEventError
    ):
        store.read_administration_event(
            event_id="EVENT-E5-CANONICAL"
        )
