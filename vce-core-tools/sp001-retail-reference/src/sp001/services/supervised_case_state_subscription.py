from threading import RLock
import time
from uuid import uuid4

from sp001.contracts.case_state_reader import CaseStateReader
from sp001.contracts.case_state_read_result import (
    BackendUnavailable, RequestRejected, TransportUnavailable,
)
from sp001.contracts.subscriber_session_policy import (
    SubscriberSessionState, SessionObservation, SessionAction,
    evaluate_subscriber_session,
)
from sp001.services.case_state_reconciliation import (
    CaseStateReconciler, ViewStatus, SessionResponseRejected,
)


class SupervisedCaseStateSubscription:
    """Own one remote view; timer ticks must be supplied independently."""

    def __init__(self, *, reader, case_id, clock=None):
        if not isinstance(reader, CaseStateReader):
            raise TypeError("reader must implement CaseStateReader")
        if clock is not None and not callable(clock):
            raise TypeError("clock must be callable")
        self._reader = reader
        self._reconciler = CaseStateReconciler(case_id=case_id)
        self._clock = time.monotonic if clock is None else clock
        self._session_id = str(uuid4())
        self._health = None
        self._terminated = False
        self._inflight = False
        self._lock = RLock()

    @property
    def session_id(self):
        return self._session_id

    @property
    def view(self):
        return self.tick()

    def _terminate(self, reason):
        self._terminated = True
        self._reconciler.terminate_session(reason=reason)

    def _observe(self, observation):
        now = self._clock()
        if self._health is None:
            if observation is SessionObservation.VALIDATED:
                self._health = SubscriberSessionState(self._session_id, now)
            elif observation in (
                SessionObservation.AUTHENTICATION_REJECTED,
                SessionObservation.PERMISSION_WITHDRAWN,
            ):
                self._terminate(observation.value)
            return
        decision = evaluate_subscriber_session(
            state=self._health, observation=observation,
            session_id=self._session_id, now=now,
        )
        self._health = decision.state
        if decision.action is SessionAction.HIDE_AND_BLOCK:
            self._terminate(decision.reason)

    def tick(self):
        with self._lock:
            if not self._terminated:
                self._observe(SessionObservation.TICK)
            return self._reconciler.view

    def refresh(self):
        with self._lock:
            self.tick()
            if self._terminated:
                raise SessionResponseRejected("session_terminated")
            if self._inflight:
                raise SessionResponseRejected("read_already_in_flight")
            request = self._reconciler.begin_read()
            self._inflight = True
        try:
            try:
                result = self._reader.read(case_id=request.case_id)
            except Exception:
                with self._lock:
                    self.tick()
                    if self._terminated:
                        raise SessionResponseRejected("session_terminated") from None
                    self._reconciler.fail_read(request=request)
                raise
            with self._lock:
                self.tick()
                if self._terminated:
                    raise SessionResponseRejected("session_terminated")
                self._reconciler.accept(request=request, result=result)
                if isinstance(result, RequestRejected) and result.status_code in (401, 403):
                    observation = (
                        SessionObservation.AUTHENTICATION_REJECTED
                        if result.status_code == 401
                        else SessionObservation.PERMISSION_WITHDRAWN
                    )
                    self._observe(observation)
                elif isinstance(result, (TransportUnavailable, BackendUnavailable)):
                    self._observe(SessionObservation.UNAVAILABLE)
                elif self._reconciler.view.status in (
                    ViewStatus.CURRENT, ViewStatus.NOT_FOUND,
                ):
                    self._observe(SessionObservation.VALIDATED)
                return self._reconciler.view
        finally:
            with self._lock:
                self._inflight = False
