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


class ConfirmationLost(Exception):
    pass


def apply_then_lose_confirmation(store, record):
    assert store.apply(record=record) is True
    raise ConfirmationLost("simulated response delivery loss")


@pytest.mark.parametrize("action", ["GRANT", "REVOKE"])
def test_confirmed_event_survives_lost_response_without_duplicate(
    tmp_path, action
):
    path = tmp_path / "grants.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)

    first = make_record()

    if action == "GRANT":
        event = first
        expected_audit = (first,)
        expected_revision = 1
        expected_revoked = False
    else:
        assert store.apply(record=first) is True
        event = replace(
            first,
            event_id="REVOKE-1",
            action=Action.REVOKE,
            recorded_at=150,
        )
        expected_audit = (first, event)
        expected_revision = 2
        expected_revoked = True

    with pytest.raises(ConfirmationLost):
        apply_then_lose_confirmation(store, event)

    reopened = SqliteCaseAccessGrants(database_path=path)

    before = reopened.read_grant_snapshot(grant_id="GRANT-1")

    assert before is not None
    assert before.revision == expected_revision
    assert before.revoked is expected_revoked
    assert reopened.read_audit() == expected_audit

    assert reopened.apply(record=event) is True

    assert reopened.read_grant_snapshot(grant_id="GRANT-1") == before
    assert reopened.read_audit() == expected_audit
