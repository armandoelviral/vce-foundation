import pytest

from sp001.contracts.subscriber_poll_schedule import SubscriberPollSchedule


@pytest.mark.parametrize("interval", [4, 5, 6])
def test_interval_is_measured_from_poll_start(interval):
    pending = SubscriberPollSchedule(100).begin(
        now=100, interval_seconds=interval,
    )
    finished = pending.finish()
    assert not finished.is_due(now=100 + interval - 0.01)
    assert finished.is_due(now=100 + interval)


def test_pending_read_prevents_overlapping_polls():
    pending = SubscriberPollSchedule(100).begin(
        now=100, interval_seconds=5,
    )
    assert not pending.is_due(now=115)
    with pytest.raises(RuntimeError, match="poll_not_due"):
        pending.begin(now=115, interval_seconds=5)


def test_delayed_completion_does_not_accumulate_missed_polls():
    finished = SubscriberPollSchedule(100).begin(
        now=100, interval_seconds=5,
    ).finish()
    pending = finished.begin(now=115, interval_seconds=6)
    assert pending.next_due_at == 121
    assert not pending.is_due(now=115)
    assert not pending.finish().is_due(now=120)


def test_completion_after_stop_cannot_restart_polling():
    pending = SubscriberPollSchedule(100).begin(
        now=100, interval_seconds=5,
    )
    stopped = pending.stop()
    completed = stopped.finish()
    assert completed.stopped
    assert not completed.in_flight
    assert not completed.is_due(now=200)
    with pytest.raises(RuntimeError, match="poll_not_due"):
        completed.begin(now=200, interval_seconds=5)


def test_stopping_is_idempotent():
    stopped = SubscriberPollSchedule(100).stop()
    assert stopped.stop() == stopped


def test_cannot_finish_without_pending_poll():
    with pytest.raises(RuntimeError, match="no_poll_in_flight"):
        SubscriberPollSchedule(100).finish()


@pytest.mark.parametrize("interval", [
    True, -1, 0, 3.99, 6.01, float("nan"), float("inf"), "5",
])
def test_invalid_interval_is_rejected(interval):
    with pytest.raises(ValueError):
        SubscriberPollSchedule(100).begin(
            now=100, interval_seconds=interval,
        )


@pytest.mark.parametrize("now", [
    True, -1, float("nan"), float("inf"), "100",
])
def test_invalid_monotonic_time_is_rejected(now):
    with pytest.raises(ValueError):
        SubscriberPollSchedule(100).is_due(now=now)


def test_poll_cannot_start_before_due_time():
    schedule = SubscriberPollSchedule(105)
    with pytest.raises(RuntimeError, match="poll_not_due"):
        schedule.begin(now=104, interval_seconds=5)
