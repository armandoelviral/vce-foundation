from dataclasses import dataclass
import math


def _seconds(value, name):
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value < 0
    ):
        raise ValueError(f"{name} must be finite nonnegative seconds")


@dataclass(frozen=True, slots=True)
class SubscriberPollSchedule:
    """Monotonic polling schedule; owns no snapshot or security decision."""

    next_due_at: float
    in_flight: bool = False
    stopped: bool = False

    def __post_init__(self):
        _seconds(self.next_due_at, "next_due_at")
        if type(self.in_flight) is not bool or type(self.stopped) is not bool:
            raise TypeError("schedule flags must be booleans")

    def is_due(self, *, now):
        _seconds(now, "now")
        return (
            not self.stopped
            and not self.in_flight
            and now >= self.next_due_at
        )

    def begin(self, *, now, interval_seconds):
        _seconds(now, "now")
        _seconds(interval_seconds, "interval_seconds")
        if not 4 <= interval_seconds <= 6:
            raise ValueError("poll interval must be between 4 and 6 seconds")
        if not self.is_due(now=now):
            raise RuntimeError("poll_not_due")
        return SubscriberPollSchedule(
            next_due_at=now + interval_seconds,
            in_flight=True,
        )

    def finish(self):
        if not self.in_flight:
            raise RuntimeError("no_poll_in_flight")
        return SubscriberPollSchedule(
            next_due_at=self.next_due_at,
            stopped=self.stopped,
        )

    def stop(self):
        return SubscriberPollSchedule(
            next_due_at=self.next_due_at,
            in_flight=self.in_flight,
            stopped=True,
        )
