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
        event_id="EVENT-E2-1",
        actor=AuthenticatedPrincipal(
            "issuer-A", "administrator-1"
        ),
        action=Action.GRANT,
        grant=CaseAccessGrant(
            "GRANT-E2-1",
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


def observe_event(store, expected):
    """
    Test-only classification of the existing audit reader.

    This is not a production reconciliation contract.
    """
    try:
        audit = store.read_audit()
    except (sqlite3.Error, OSError):
        return "READ_UNAVAILABLE"

    matching_ids = [
        item for item in audit
        if item.event_id == expected.event_id
    ]

    if not matching_ids:
        return "EVENT_NOT_FOUND"

    if len(matching_ids) != 1:
        return "READ_INVALID"

    if matching_ids[0] == expected:
        return "EXACT_MATCH"

    return "EVENT_CONFLICT"


def test_exact_event_is_observed_after_reopen(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)
    command = make_record()

    assert store.apply(record=command) is True

    reopened = SqliteCaseAccessGrants(
        database_path=path
    )

    assert observe_event(
        reopened, command
    ) == "EXACT_MATCH"


def test_same_event_id_with_different_record_is_conflict(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)
    command = make_record()

    assert store.apply(record=command) is True

    conflicting = replace(
        command,
        recorded_at=101,
    )

    reopened = SqliteCaseAccessGrants(
        database_path=path
    )

    assert observe_event(
        reopened, conflicting
    ) == "EVENT_CONFLICT"


def test_missing_event_is_only_observed_absence(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)
    command = make_record()

    assert store.apply(record=command) is True

    absent = replace(
        command,
        event_id="EVENT-E2-MISSING",
    )

    reopened = SqliteCaseAccessGrants(
        database_path=path
    )

    assert observe_event(
        reopened, absent
    ) == "EVENT_NOT_FOUND"

    assert reopened.read_audit() == (command,)


def test_failed_read_is_not_classified_as_absence(tmp_path):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)
    command = make_record()

    assert store.apply(record=command) is True

    class UnavailableReader:
        def read_audit(self):
            raise sqlite3.OperationalError(
                "injected read failure"
            )

    assert observe_event(
        UnavailableReader(), command
    ) == "READ_UNAVAILABLE"

    reopened = SqliteCaseAccessGrants(
        database_path=path
    )

    assert reopened.read_audit() == (command,)
