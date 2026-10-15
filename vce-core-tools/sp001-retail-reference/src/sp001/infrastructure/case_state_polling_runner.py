import math
import random
import threading
import time

from sp001.contracts.subscriber_poll_schedule import SubscriberPollSchedule
from sp001.services.case_state_reconciliation import (
    SessionResponseRejected, ViewStatus,
)
from sp001.services.supervised_case_state_subscription import (
    SupervisedCaseStateSubscription,
)


class CaseStatePollingRunner:
    """One polling worker and one independent session watcher.

    No background work starts during construction. A runner is single-use.
    Clock injection must match the subscription's monotonic clock.
    """

    def __init__(self, *, subscription, clock=None, interval_provider=None):
        if not isinstance(subscription, SupervisedCaseStateSubscription):
            raise TypeError("subscription must be supervised")
        if clock is not None and not callable(clock):
            raise TypeError("clock must be callable")
        if interval_provider is not None and not callable(interval_provider):
            raise TypeError("interval_provider must be callable")
        self._subscription = subscription
        self._clock = time.monotonic if clock is None else clock
        self._interval = (
            (lambda: random.uniform(4, 6))
            if interval_provider is None else interval_provider
        )
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._started = False
        self._closed = False
        self._failure = None
        self._threads = ()

    @property
    def view(self):
        return self._subscription.view

    @property
    def failure(self):
        with self._lock:
            return self._failure

    @property
    def workers_alive(self):
        with self._lock:
            return sum(thread.is_alive() for thread in self._threads)

    def start(self):
        with self._lock:
            if self._started or self._closed:
                raise RuntimeError("runner_cannot_restart")
            self._started = True
            self._threads = (
                threading.Thread(target=self._poll, daemon=True),
                threading.Thread(target=self._watch, daemon=True),
            )
            try:
                for thread in self._threads:
                    thread.start()
            except Exception:
                self._closed = True
                self._stop.set()
                self._subscription.close(reason="polling_start_failed")
                raise

    def _failed(self):
        # Retain no exception object, traceback, token or response payload.
        with self._lock:
            self._failure = "polling_runtime_failed"
        self._stop.set()
        self._subscription.close(reason="polling_runtime_failed")

    def _poll(self):
        try:
            schedule = SubscriberPollSchedule(self._clock())
            while not self._stop.is_set():
                now = self._clock()
                if not schedule.is_due(now=now):
                    self._stop.wait(0.05)
                    continue
                schedule = schedule.begin(
                    now=now, interval_seconds=self._interval(),
                )
                try:
                    view = self._subscription.refresh()
                except SessionResponseRejected:
                    if (
                        not self._stop.is_set()
                        and self._subscription.view.status is not ViewStatus.BLOCKED
                    ):
                        self._failed()
                    self._stop.set()
                    return
                finally:
                    schedule = schedule.finish()
                if view.status is ViewStatus.BLOCKED:
                    self._stop.set()
                    return
                # Do not retain a previous snapshot while waiting.
                del view
        except Exception:
            self._failed()

    def _watch(self):
        try:
            while not self._stop.is_set():
                if self._subscription.tick().status is ViewStatus.BLOCKED:
                    self._stop.set()
                    return
                self._stop.wait(0.05)
        except Exception:
            self._failed()

    def close(self, *, join_timeout_seconds=2):
        if (
            isinstance(join_timeout_seconds, bool)
            or not isinstance(join_timeout_seconds, (int, float))
            or not math.isfinite(join_timeout_seconds)
            or join_timeout_seconds < 0
        ):
            raise ValueError("join timeout must be finite nonnegative seconds")
        with self._lock:
            self._closed = True
            threads = self._threads
        self._stop.set()
        self._subscription.close()
        deadline = time.monotonic() + join_timeout_seconds
        for thread in threads:
            if thread is not threading.current_thread() and thread.ident is not None:
                thread.join(max(0, deadline - time.monotonic()))
        return self.workers_alive == 0
