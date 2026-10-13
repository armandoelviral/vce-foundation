from dataclasses import replace

import pytest

from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_context import (
    CaseAccessPermission, CaseAccessOperation,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action,
    GrantAdministrationRecord,
)
from sp001.services.case_access_grant_administration import (
    administer_case_access_grant,
)


def record(action=Action.GRANT):
    return GrantAdministrationRecord(
        event_id="EVENT-001",
        actor=AuthenticatedPrincipal("issuer-A", "administrator-1"),
        action=action,
        grant=CaseAccessGrant(
            grant_id="GRANT-001",
            principal=AuthenticatedPrincipal("issuer-A", "subscriber-1"),
            permission=CaseAccessPermission(
                "CASE-001", CaseAccessOperation.READ_STATE,
            ),
            valid_from=100, expires_at=200,
        ),
        recorded_at=100,
    )


class Store:
    def __init__(self):
        self.calls = []
        self.result = True

    def apply(self, *, record):
        self.calls.append(record)
        return self.result


class Policy:
    def __init__(self, decision):
        self.decision = decision
        self.calls = []

    def may_administer(self, *, actor, action, grant):
        self.calls.append((actor, action, grant))
        return self.decision


@pytest.mark.parametrize("action", [Action.GRANT, Action.REVOKE])
def test_exact_actor_action_and_grant_are_authorized_before_storage(action):
    command = record(action)
    store = Store()
    policy = Policy(True)
    assert administer_case_access_grant(
        store=store, policy=policy, record=command,
    )
    assert policy.calls == [(command.actor, action, command.grant)]
    assert store.calls == [command]


@pytest.mark.parametrize("action", [Action.GRANT, Action.REVOKE])
def test_denial_never_invokes_storage(action):
    store = Store()
    with pytest.raises(PermissionError):
        administer_case_access_grant(
            store=store, policy=Policy(False), record=record(action),
        )
    assert store.calls == []


@pytest.mark.parametrize("decision", [None, 0, 1, "yes"])
def test_invalid_policy_result_never_invokes_storage(decision):
    store = Store()
    with pytest.raises(TypeError):
        administer_case_access_grant(
            store=store, policy=Policy(decision), record=record(),
        )
    assert store.calls == []


def test_policy_failure_propagates_without_storage():
    class FailingPolicy:
        def may_administer(self, **kwargs):
            raise RuntimeError("policy unavailable")

    store = Store()
    with pytest.raises(RuntimeError):
        administer_case_access_grant(
            store=store, policy=FailingPolicy(), record=record(),
        )
    assert store.calls == []


def test_unknown_grant_result_remains_false():
    store = Store()
    store.result = False
    assert not administer_case_access_grant(
        store=store, policy=Policy(True), record=record(Action.REVOKE),
    )


@pytest.mark.parametrize("field,value", [
    ("event_id", ""), ("actor", None), ("action", "GRANT"),
    ("grant", None), ("recorded_at", True), ("recorded_at", -1),
])
def test_invalid_audit_record_is_rejected(field, value):
    with pytest.raises((TypeError, ValueError)):
        replace(record(), **{field: value})
