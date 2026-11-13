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
from sp001.services.case_access_grant_administration import (
    administer_case_access_grant,
)


def make_record():
    return GrantAdministrationRecord(
        event_id="EVENT-D5-1",
        actor=AuthenticatedPrincipal("issuer-A", "administrator-1"),
        action=Action.GRANT,
        grant=CaseAccessGrant(
            "GRANT-D5-1",
            AuthenticatedPrincipal("issuer-A", "subscriber-1"),
            CaseAccessPermission(
                "CASE-001", CaseAccessOperation.READ_STATE
            ),
            100,
            200,
        ),
        recorded_at=100,
    )


def test_authorization_precedes_storage():
    calls = []
    command = make_record()

    class Policy:
        def may_administer(self, *, actor, action, grant):
            calls.append(("authorize", actor, action, grant))
            return True

    class Store:
        def apply(self, *, record):
            calls.append(("persist", record))
            return True

    assert administer_case_access_grant(
        store=Store(),
        policy=Policy(),
        record=command,
    ) is True

    assert calls == [
        (
            "authorize",
            command.actor,
            command.action,
            command.grant,
        ),
        ("persist", command),
    ]


def test_policy_change_after_authorization_is_not_revalidated():
    calls = []
    command = make_record()
    state = {"allowed": True}

    class Policy:
        def may_administer(self, *, actor, action, grant):
            calls.append("authorize")
            decision = state["allowed"]
            state["allowed"] = False
            return decision

    class Store:
        def apply(self, *, record):
            calls.append("persist")
            assert state["allowed"] is False
            return True

    assert administer_case_access_grant(
        store=Store(),
        policy=Policy(),
        record=command,
    ) is True

    assert calls == ["authorize", "persist"]
    assert state["allowed"] is False
