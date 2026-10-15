import time

import jwt
import pytest

from test_authenticated_case_state_https import secured_host
from sp001.contracts.case_access_grant_administration import GrantAdministrationAction
from sp001.infrastructure.remote_case_state_subscription_composition import (
    compose_remote_case_state_subscription,
)
from sp001.services.case_state_reconciliation import (
    SessionResponseRejected, ViewStatus,
)


def compose(policy, provider):
    return compose_remote_case_state_subscription(
        endpoint=policy["endpoint"], case_id="CASE-001",
        credential_provider=provider, timeout_seconds=2,
        max_response_bytes=4096, ca_file=policy["ca_file"],
        clock=lambda: 100.0,
    )


def test_durable_revocation_blocks_live_token_and_withdraws_owned_snapshot(
    secured_host,
):
    _, issue, events, policy = secured_host
    credential = issue()
    provider_calls = []

    def provider():
        provider_calls.append("credential")
        return credential

    session = compose(policy, provider)
    assert events == []
    assert session.refresh().status is ViewStatus.CURRENT

    audit = policy["revoke"]("CASE-001")
    assert audit[-1].action is GrantAdministrationAction.REVOKE
    assert audit[-1].grant.grant_id == "GRANT-CASE-001"
    assert time.time() < jwt.decode(
        credential, options={"verify_signature": False},
    )["exp"]

    blocked = session.refresh()
    assert blocked.status is ViewStatus.BLOCKED
    assert blocked.reason == "PERMISSION_WITHDRAWN"
    assert blocked.last_valid_state is None
    assert events == [
        "authenticate", "authorize", "read",
        "authenticate", "authorize",
    ]
    assert provider_calls == ["credential", "credential"]

    before = list(events)
    with pytest.raises(SessionResponseRejected):
        session.refresh()
    assert session.view is blocked
    assert events == before
    assert provider_calls == ["credential", "credential"]

    # A fresh session with the same live token still encounters revoked authority.
    another = compose(policy, provider)
    assert another.session_id != session.session_id
    denied = another.refresh()
    assert denied.status is ViewStatus.BLOCKED
    assert denied.last_valid_state is None
    assert events[-2:] == ["authenticate", "authorize"]
    assert events.count("read") == 1


def test_401_clears_view_and_new_credential_cannot_revive_old_session(secured_host):
    _, issue, events, policy = secured_host
    current = {"credential": issue()}
    session = compose(policy, lambda: current["credential"])
    assert session.refresh().last_valid_state is not None

    current["credential"] = "broken"
    blocked = session.refresh()
    assert blocked.status is ViewStatus.BLOCKED
    assert blocked.reason == "AUTHENTICATION_REJECTED"
    assert blocked.last_valid_state is None
    assert events == ["authenticate", "authorize", "read", "authenticate"]

    current["credential"] = issue()
    before = list(events)
    with pytest.raises(SessionResponseRejected):
        session.refresh()
    assert session.view is blocked
    assert events == before

    # Explicit creation of a new session is distinct from automatic revival.
    replacement = compose(policy, lambda: current["credential"])
    assert replacement.session_id != session.session_id
    assert replacement.refresh().status is ViewStatus.CURRENT
    assert session.view is blocked
