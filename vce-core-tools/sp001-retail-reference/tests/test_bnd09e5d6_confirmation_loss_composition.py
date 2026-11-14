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
from sp001.contracts.case_grant_administration_reconciliation import (
    AdministrationReconciliationStatus as Status,
)
from sp001.infrastructure.sqlite_case_access_grants import (
    SqliteCaseAccessGrants,
)
from sp001.services.case_grant_administration_reconciliation import (
    reconcile_administration_event,
)


class ConfirmationLost(Exception):
    pass


def make_record():
    return GrantAdministrationRecord(
        event_id="EVENT-D6-GRANT",
        actor=AuthenticatedPrincipal("issuer-A", "administrator-1"),
        action=Action.GRANT,
        grant=CaseAccessGrant(
            "GRANT-D6-1",
            AuthenticatedPrincipal("issuer-A", "subscriber-1"),
            CaseAccessPermission(
                "CASE-D6-1",
                CaseAccessOperation.READ_STATE,
            ),
            100,
            200,
        ),
        recorded_at=100,
    )


@pytest.mark.parametrize("action", [Action.GRANT, Action.REVOKE])
def test_confirmation_loss_reconciles_without_reapplying(
    tmp_path, action
):
    path = tmp_path / "administration.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)

    first = make_record()

    if action is Action.GRANT:
        event = first
    else:
        assert store.apply(record=first) is True
        event = replace(
            first,
            event_id="EVENT-D6-REVOKE",
            action=Action.REVOKE,
            recorded_at=150,
        )

    with pytest.raises(ConfirmationLost):
        assert store.apply(record=event) is True
        raise ConfirmationLost("simulated confirmation loss")

    reopened = SqliteCaseAccessGrants(database_path=path)

    before_snapshot = reopened.read_grant_snapshot(
        grant_id=event.grant.grant_id
    )
    before_audit = reopened.read_audit()

    result = reconcile_administration_event(
        reader=reopened,
        expected=event,
    )

    assert result.event_id == event.event_id
    assert result.status is Status.EXACT_MATCH

    assert reopened.read_grant_snapshot(
        grant_id=event.grant.grant_id
    ) == before_snapshot
    assert reopened.read_audit() == before_audit


class ReadOnlyAdministrationEventView:
    __slots__ = ("_read", "calls")

    def __init__(self, store):
        self._read = store.read_administration_event
        self.calls = []

    def read_administration_event(self, *, event_id):
        self.calls.append(event_id)
        return self._read(event_id=event_id)


@pytest.mark.parametrize("action", [Action.GRANT, Action.REVOKE])
def test_reconciliation_uses_read_only_capability(tmp_path, action):
    path = tmp_path / "read_only.sqlite3"
    store = SqliteCaseAccessGrants(database_path=path)

    first = make_record()

    if action is Action.GRANT:
        event = first
    else:
        assert store.apply(record=first) is True
        event = replace(
            first,
            event_id="EVENT-D6-REVOKE",
            action=Action.REVOKE,
            recorded_at=150,
        )

    assert store.apply(record=event) is True

    reopened = SqliteCaseAccessGrants(database_path=path)
    reader = ReadOnlyAdministrationEventView(reopened)

    assert not hasattr(reader, "apply")
    assert not hasattr(reader, "read_audit")

    before = reopened.read_audit()

    result = reconcile_administration_event(
        reader=reader,
        expected=event,
    )

    assert result.status is Status.EXACT_MATCH
    assert reader.calls == [event.event_id]
    assert reopened.read_audit() == before
