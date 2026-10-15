from dataclasses import dataclass, replace
from enum import Enum
import math


class SessionObservation(str, Enum):
    VALIDATED = "VALIDATED"
    UNAVAILABLE = "UNAVAILABLE"
    AUTHENTICATION_REJECTED = "AUTHENTICATION_REJECTED"
    PERMISSION_WITHDRAWN = "PERMISSION_WITHDRAWN"
    TICK = "TICK"


class SessionTermination(str, Enum):
    AUTHENTICATION_REJECTED = "AUTHENTICATION_REJECTED"
    PERMISSION_WITHDRAWN = "PERMISSION_WITHDRAWN"
    VERIFICATION_UNAVAILABLE = "VERIFICATION_UNAVAILABLE"


class SessionAction(str, Enum):
    KEEP = "KEEP"
    WARN = "WARN"
    HIDE_AND_BLOCK = "HIDE_AND_BLOCK"
    IGNORE = "IGNORE"


def _time(value, name):
    if (
        isinstance(value, bool) or not isinstance(value, (int, float))
        or not math.isfinite(value) or value < 0
    ):
        raise ValueError(f"{name} must be finite nonnegative monotonic seconds")


@dataclass(frozen=True, slots=True)
class SubscriberSessionState:
    """State of a session with an already validated view; contains no snapshot."""

    session_id: str
    last_validated_at: float
    consecutive_failures: int = 0
    termination: SessionTermination | None = None

    def __post_init__(self):
        if not isinstance(self.session_id, str) or not self.session_id.strip():
            raise ValueError("session_id must be nonempty")
        _time(self.last_validated_at, "last_validated_at")
        if type(self.consecutive_failures) is not int or self.consecutive_failures < 0:
            raise ValueError("consecutive_failures must be a nonnegative integer")
        if self.termination is not None and not isinstance(
            self.termination, SessionTermination,
        ):
            raise TypeError("termination must be a SessionTermination")


@dataclass(frozen=True, slots=True)
class SubscriberSessionDecision:
    state: SubscriberSessionState
    action: SessionAction
    reason: str


def evaluate_subscriber_session(
    *, state: SubscriberSessionState, observation: SessionObservation,
    session_id: str, now: float,
) -> SubscriberSessionDecision:
    """Apply visibility policy; performs no authentication, I/O or memory erasure.

    VALIDATED means a response has already passed identity, contract and access
    checks. The caller supplies a monotonic clock and a unique session generation.
    """
    if not isinstance(state, SubscriberSessionState):
        raise TypeError("state must be a SubscriberSessionState")
    if not isinstance(observation, SessionObservation):
        raise TypeError("observation must be a SessionObservation")
    if not isinstance(session_id, str) or not session_id.strip():
        raise ValueError("session_id must be nonempty")
    _time(now, "now")
    if now < state.last_validated_at:
        raise ValueError("monotonic time cannot precede last validation")
    if state.termination is not None:
        return SubscriberSessionDecision(state, SessionAction.IGNORE, "session_terminated")

    if session_id == state.session_id:
        terminal = {
            SessionObservation.AUTHENTICATION_REJECTED:
                SessionTermination.AUTHENTICATION_REJECTED,
            SessionObservation.PERMISSION_WITHDRAWN:
                SessionTermination.PERMISSION_WITHDRAWN,
        }.get(observation)
        if terminal is not None:
            return SubscriberSessionDecision(
                replace(state, termination=terminal),
                SessionAction.HIDE_AND_BLOCK, terminal.value,
            )

    # A successful response arriving after the deadline cannot revive the session.
    if now - state.last_validated_at >= 10:
        return SubscriberSessionDecision(
            replace(state, termination=SessionTermination.VERIFICATION_UNAVAILABLE),
            SessionAction.HIDE_AND_BLOCK, "validation_deadline_exceeded",
        )
    if session_id != state.session_id:
        return SubscriberSessionDecision(state, SessionAction.IGNORE, "session_mismatch")
    if observation is SessionObservation.VALIDATED:
        return SubscriberSessionDecision(
            replace(state, last_validated_at=now, consecutive_failures=0),
            SessionAction.KEEP, "validation_confirmed",
        )
    if observation is SessionObservation.UNAVAILABLE:
        updated = replace(state, consecutive_failures=state.consecutive_failures + 1)
        if updated.consecutive_failures >= 2:
            return SubscriberSessionDecision(
                replace(updated, termination=SessionTermination.VERIFICATION_UNAVAILABLE),
                SessionAction.HIDE_AND_BLOCK, "consecutive_verification_failures",
            )
        return SubscriberSessionDecision(updated, SessionAction.WARN, "synchronization_pending")
    return SubscriberSessionDecision(state, SessionAction.KEEP, "deadline_not_reached")
