import threading
import time

import pytest

from test_authenticated_case_state_https import secured_host
from sp001.infrastructure.remote_case_state_polling_composition import (
    compose_remote_case_state_polling,
)
from sp001.services.case_state_reconciliation import ViewStatus


def eventually(predicate):
    deadline = time.monotonic() + 3
    while time.monotonic() < deadline:
        if predicate():
            return
        threading.Event().wait(0.01)
    assert predicate()


def compose(policy, provider, now):
    return compose_remote_case_state_polling(
        endpoint=policy["endpoint"],
        case_id="CASE-001",
        credential_provider=provider,
        timeout_seconds=2,
        max_response_bytes=4096,
        ca_file=policy["ca_file"],
        clock=lambda: now[0],
        interval_provider=lambda: 5,
    )


def test_https_polling_observes_durable_revocation_with_same_token(secured_host):
    _, issue, events, policy = secured_host
    token = issue()
    credentials = []

    def provider():
        credentials.append("called")
        return token

    now = [100]
    runner = compose(policy, provider, now)
    assert events == []
    assert credentials == []
    assert runner.workers_alive == 0

    try:
        runner.start()
        eventually(lambda: runner.view.status is ViewStatus.CURRENT)
        assert runner.view.last_valid_state is not None

        policy["revoke"]("CASE-001")
        now[0] = 105
        eventually(lambda: runner.view.status is ViewStatus.BLOCKED)
        eventually(lambda: runner.workers_alive == 0)

        blocked = runner.view
        assert blocked.reason == "PERMISSION_WITHDRAWN"
        assert blocked.last_valid_state is None
        assert events == [
            "authenticate", "authorize", "read",
            "authenticate", "authorize",
        ]
        assert credentials == ["called", "called"]
        assert runner.failure is None

        with pytest.raises(RuntimeError, match="runner_cannot_restart"):
            runner.start()
        assert runner.view is blocked
    finally:
        runner.close()


def test_https_expired_token_blocks_without_reading_case(secured_host):
    _, issue, events, policy = secured_host
    runner = compose(policy, lambda: issue(expired=True), [100])
    try:
        runner.start()
        eventually(lambda: runner.view.status is ViewStatus.BLOCKED)
        eventually(lambda: runner.workers_alive == 0)
        assert runner.view.reason == "AUTHENTICATION_REJECTED"
        assert runner.view.last_valid_state is None
        assert events == ["authenticate"]
        assert runner.failure is None
    finally:
        runner.close()


def test_close_after_https_read_withdraws_owned_snapshot(secured_host):
    _, issue, events, policy = secured_host
    token = issue()
    runner = compose(policy, lambda: token, [100])
    try:
        runner.start()
        eventually(lambda: runner.view.status is ViewStatus.CURRENT)
        assert runner.close()
        blocked = runner.view
        assert blocked.status is ViewStatus.BLOCKED
        assert blocked.last_valid_state is None
        assert blocked.reason == "subscriber_closed"
        assert events == ["authenticate", "authorize", "read"]
        assert runner.close()
        assert runner.view is blocked
    finally:
        runner.close()
