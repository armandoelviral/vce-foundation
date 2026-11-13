import sqlite3
from dataclasses import replace
from unittest.mock import Mock

import pytest

from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationRecord,
)
from sp001.contracts.case_grant_administration_reconciliation import (
    AdministrationReconciliationStatus as Status,
)
from sp001.infrastructure.sqlite_case_access_grants import (
    InvalidPersistedAdministrationEventError,
)
from sp001.services.case_grant_administration_reconciliation import (
    reconcile_administration_event,
)


def expected_record():
    from sp001.contracts.case_access_grant_administration import (
        GrantAdministrationAction,
    )
    from sp001.contracts.case_access_grant import CaseAccessGrant
    from sp001.contracts.case_access_context import (
        CaseAccessOperation,
        CaseAccessPermission,
    )
    from sp001.contracts.case_read_access import AuthenticatedPrincipal

    return GrantAdministrationRecord(
        event_id="EVENT-D5-1",
        actor=AuthenticatedPrincipal(
            issuer="issuer-A",
            subject="administrator-1",
        ),
        action=GrantAdministrationAction.GRANT,
        grant=CaseAccessGrant(
            grant_id="GRANT-D5-1",
            principal=AuthenticatedPrincipal(
                issuer="issuer-A",
                subject="subscriber-1",
            ),
            permission=CaseAccessPermission(
                case_id="CASE-D5-1",
                operation=CaseAccessOperation.READ_STATE,
            ),
            valid_from=100,
            expires_at=200,
        ),
        recorded_at=100,
    )


def reader_returning(value):
    reader = Mock()
    reader.read_administration_event.return_value = value
    return reader


def reader_raising(error):
    reader = Mock()
    reader.read_administration_event.side_effect = error
    return reader


def reconcile(reader, expected):
    return reconcile_administration_event(
        reader=reader,
        expected=expected,
    )


def test_exact_match():
    expected = expected_record()
    reader = reader_returning(expected)

    result = reconcile(reader, expected)

    assert result.event_id == expected.event_id
    assert result.status is Status.EXACT_MATCH
    reader.read_administration_event.assert_called_once_with(
        event_id=expected.event_id
    )


def test_event_conflict():
    expected = expected_record()
    conflicting = replace(expected, recorded_at=101)

    result = reconcile(reader_returning(conflicting), expected)

    assert result.status is Status.EVENT_CONFLICT


def test_event_not_found():
    expected = expected_record()

    result = reconcile(reader_returning(None), expected)

    assert result.status is Status.EVENT_NOT_FOUND


def test_read_unavailable():
    expected = expected_record()

    result = reconcile(
        reader_raising(sqlite3.OperationalError("database unavailable")),
        expected,
    )

    assert result.status is Status.READ_UNAVAILABLE


def test_read_invalid():
    expected = expected_record()

    result = reconcile(
        reader_raising(
            InvalidPersistedAdministrationEventError(
                "invalid persisted administrative event"
            )
        ),
        expected,
    )

    assert result.status is Status.READ_INVALID


@pytest.mark.parametrize(
    "error",
    [
        RuntimeError("unexpected failure"),
        ValueError("unexpected value"),
        TypeError("unexpected type"),
    ],
)
def test_unclassified_errors_propagate(error):
    expected = expected_record()

    with pytest.raises(type(error), match=str(error)):
        reconcile(reader_raising(error), expected)


def test_rejects_invalid_expected_record():
    with pytest.raises(TypeError):
        reconcile(reader_returning(None), None)


def test_rejects_invalid_reader():
    with pytest.raises(TypeError):
        reconcile(None, expected_record())


@pytest.mark.parametrize(
    "field,value",
    [
        ("event_id", "EVENT-D5-OTHER"),
        ("recorded_at", 101),
        ("action", "REVOKE"),
    ],
)
def test_different_persisted_event_is_not_exact_match(field, value):
    expected = expected_record()

    if field == "action":
        from sp001.contracts.case_access_grant_administration import (
            GrantAdministrationAction,
        )
        value = GrantAdministrationAction.REVOKE

    observed = replace(expected, **{field: value})
    result = reconcile(reader_returning(observed), expected)

    assert result.status is Status.EVENT_CONFLICT


def test_invalid_reader_response_is_rejected():
    expected = expected_record()

    with pytest.raises(TypeError):
        reconcile(reader_returning({"event_id": expected.event_id}), expected)


def test_reader_is_called_only_once():
    expected = expected_record()
    reader = reader_returning(expected)

    reconcile(reader, expected)

    assert reader.read_administration_event.call_count == 1


def test_reconciles_real_persisted_event(tmp_path):
    from sp001.infrastructure.sqlite_case_access_grants import (
        SqliteCaseAccessGrants,
    )

    store = SqliteCaseAccessGrants(
        database_path=tmp_path / "reconciliation.sqlite3"
    )
    expected = expected_record()

    assert store.apply(record=expected) is True

    result = reconcile(reader=store, expected=expected)

    assert result.event_id == expected.event_id
    assert result.status is Status.EXACT_MATCH


def test_reconciles_real_absent_event(tmp_path):
    from sp001.infrastructure.sqlite_case_access_grants import (
        SqliteCaseAccessGrants,
    )

    store = SqliteCaseAccessGrants(
        database_path=tmp_path / "reconciliation.sqlite3"
    )
    expected = expected_record()

    result = reconcile(reader=store, expected=expected)

    assert result.status is Status.EVENT_NOT_FOUND
