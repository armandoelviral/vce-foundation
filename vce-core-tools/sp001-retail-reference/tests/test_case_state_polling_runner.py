import threading
import time

import pytest

from test_case_state_reconciliation import state
from sp001.contracts.case_state_read_result import Found, RequestRejected
from sp001.infrastructure.case_state_polling_runner import CaseStatePollingRunner
from sp001.services.case_state_reconciliation import ViewStatus
from sp001.services.supervised_case_state_subscription import (
    SupervisedCaseStateSubscription,
)


def eventually(predicate):
    deadline = time.monotonic() + 2
    while time.monotonic() < deadline:
        if predicate():
            return
        threading.Event().wait(0.01)
    assert predicate()


def build(reader):
    now = [100]
    subscription = SupervisedCaseStateSubscription(
        reader=reader, case_id="CASE-001", clock=lambda: now[0],
    )
    runner = CaseStatePollingRunner(
        subscription=subscription, clock=lambda: now[0],
        interval_provider=lambda: 5,
    )
    return now, subscription, runner


def test_construction_is_idle_and_close_prevents_start():
    class Reader:
        def read(self, *, case_id):
            pytest.fail("unexpected network read")
    _, subscription, runner = build(Reader())
    assert runner.workers_alive == 0
    assert runner.close()
    assert subscription.view.status is ViewStatus.BLOCKED
    with pytest.raises(RuntimeError, match="runner_cannot_restart"):
        runner.start()


def test_403_stops_polling_and_withdraws_snapshot():
    class Reader:
        calls = 0
        def read(self, *, case_id):
            self.calls += 1
            return (
                Found(state()) if self.calls == 1
                else RequestRejected(403, "forbidden")
            )
    reader = Reader()
    now, subscription, runner = build(reader)
    try:
        runner.start()
        eventually(lambda: subscription.view.status is ViewStatus.CURRENT)
        now[0] = 105
        eventually(lambda: subscription.view.status is ViewStatus.BLOCKED)
        eventually(lambda: runner.workers_alive == 0)
        assert subscription.view.last_valid_state is None
        assert reader.calls == 2
        assert runner.failure is None
        with pytest.raises(RuntimeError, match="runner_cannot_restart"):
            runner.start()
    finally:
        runner.close()


def test_watcher_blocks_during_pending_read_and_late_response_is_rejected():
    entered = threading.Event()
    release = threading.Event()

    class Reader:
        calls = 0
        def read(self, *, case_id):
            self.calls += 1
            if self.calls == 2:
                entered.set()
                if not release.wait(3):
                    raise RuntimeError("test release missing")
                return Found(state(9))
            return Found(state())

    reader = Reader()
    now, subscription, runner = build(reader)
    try:
        runner.start()
        eventually(lambda: subscription.view.status is ViewStatus.CURRENT)
        now[0] = 105
        assert entered.wait(2)
        now[0] = 110
        # Observe owned reconciler directly: this assertion must not call
        # subscription.view, whose getter itself triggers a tick.
        eventually(
            lambda: subscription._reconciler.view.status is ViewStatus.BLOCKED
        )
        blocked = subscription._reconciler.view
        assert blocked.last_valid_state is None
        assert reader.calls == 2
        release.set()
        eventually(lambda: runner.workers_alive == 0)
        assert subscription.view is blocked
        assert runner.failure is None
    finally:
        release.set()
        runner.close()


def test_close_invalidates_pending_response_without_waiting_for_network():
    entered = threading.Event()
    release = threading.Event()

    class Reader:
        def read(self, *, case_id):
            entered.set()
            release.wait(3)
            return Found(state())

    _, subscription, runner = build(Reader())
    try:
        runner.start()
        assert entered.wait(2)
        assert not runner.close(join_timeout_seconds=0)
        blocked = subscription.view
        assert blocked.status is ViewStatus.BLOCKED
        assert blocked.last_valid_state is None
        release.set()
        eventually(lambda: runner.workers_alive == 0)
        assert subscription.view is blocked
    finally:
        release.set()
        runner.close()


def test_unclassified_reader_error_is_recorded_without_payload():
    class Reader:
        def read(self, *, case_id):
            raise RuntimeError("sensitive response body")
    _, subscription, runner = build(Reader())
    try:
        runner.start()
        eventually(lambda: runner.workers_alive == 0)
        assert runner.failure == "polling_runtime_failed"
        assert subscription.view.status is ViewStatus.BLOCKED
        assert subscription.view.last_valid_state is None
    finally:
        runner.close()
