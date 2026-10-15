import threading
import time

import pytest

from test_case_state_reconciliation import state
from sp001.contracts.case_state_read_result import (
    Found, RequestRejected, TransportUnavailable,
)
from sp001.services.case_state_reconciliation import (
    CaseStateReconciler, SessionResponseRejected, ViewStatus,
)
from sp001.services.supervised_case_state_subscription import (
    SupervisedCaseStateSubscription,
)


class Reader:
    def __init__(self):
        self.result = Found(state())
        self.calls = 0

    def read(self, *, case_id):
        self.calls += 1
        return self.result


def populated(clock):
    reader = Reader()
    session = SupervisedCaseStateSubscription(
        reader=reader, case_id="CASE-001", clock=clock,
    )
    session.refresh()
    return reader, session


def test_403_withdraws_snapshot_and_blocks_reads():
    reader, session = populated(lambda: 100)
    reader.result = RequestRejected(403, "forbidden")
    blocked = session.refresh()
    assert blocked.status is ViewStatus.BLOCKED
    assert blocked.last_valid_state is None
    assert blocked.reason == "PERMISSION_WITHDRAWN"
    calls = reader.calls
    with pytest.raises(SessionResponseRejected):
        session.refresh()
    assert reader.calls == calls
    assert session.view is blocked


def test_second_failure_withdraws_snapshot():
    now = [100]
    reader, session = populated(lambda: now[0])
    reader.result = TransportUnavailable("timeout")
    now[0] = 104
    assert session.refresh().last_valid_state is not None
    now[0] = 108
    assert session.refresh().last_valid_state is None
    assert session.view.reason == "consecutive_verification_failures"


def test_independent_timer_expires_without_network_response():
    now = [100]
    _, session = populated(lambda: now[0])
    now[0] = 110
    assert session.tick().status is ViewStatus.BLOCKED
    assert session.view.last_valid_state is None


def test_wall_clock_changes_do_not_change_deadline(monkeypatch):
    now = [100]
    _, session = populated(lambda: now[0])
    monkeypatch.setattr(time, "time", lambda: -1000000)
    now[0] = 109
    assert session.tick().last_valid_state is not None
    monkeypatch.setattr(time, "time", lambda: 9999999999)
    now[0] = 110
    assert session.tick().last_valid_state is None


def test_termination_invalidates_reconciler_request():
    reconciler = CaseStateReconciler(case_id="CASE-001")
    request = reconciler.begin_read()
    reconciler.accept(request=request, result=Found(state()))
    pending = reconciler.begin_read()
    blocked = reconciler.terminate_session(reason="PERMISSION_WITHDRAWN")
    assert blocked.last_valid_state is None
    with pytest.raises(SessionResponseRejected):
        reconciler.accept(request=pending, result=Found(state(9)))
    assert reconciler.view is blocked


def test_real_15_second_response_cannot_repopulate_view():
    reader, session = populated(None)
    entered = threading.Event()
    errors = []

    def delayed_read(*, case_id):
        entered.set()
        threading.Event().wait(15)
        return Found(state(9))

    reader.read = delayed_read

    def refresh():
        try:
            session.refresh()
        except Exception as error:
            errors.append(error)

    worker = threading.Thread(target=refresh, daemon=True)
    worker.start()
    try:
        assert entered.wait(timeout=2)
        threading.Event().wait(10.1)
        blocked = session.tick()
        assert blocked.status is ViewStatus.BLOCKED
        assert blocked.last_valid_state is None
        worker.join(timeout=7)
        assert not worker.is_alive()
        assert len(errors) == 1
        assert isinstance(errors[0], SessionResponseRejected)
        assert session.view is blocked
    finally:
        worker.join(timeout=17)
