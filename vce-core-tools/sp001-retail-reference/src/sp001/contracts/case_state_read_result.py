from dataclasses import dataclass
from typing import TypeAlias

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState


def _text(value: object, name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True, slots=True)
class Found:
    state: CaseAuthoritativeState

    def __post_init__(self) -> None:
        if not isinstance(self.state, CaseAuthoritativeState):
            raise TypeError("state must be a CaseAuthoritativeState")


@dataclass(frozen=True, slots=True)
class NotFound:
    """Explicit domain absence; an HTTP status alone cannot establish this."""

    case_id: str

    def __post_init__(self) -> None:
        _text(self.case_id, "case_id")


@dataclass(frozen=True, slots=True)
class TransportUnavailable:
    cause: str

    def __post_init__(self) -> None:
        _text(self.cause, "cause")


@dataclass(frozen=True, slots=True)
class BackendUnavailable:
    status_code: int

    def __post_init__(self) -> None:
        if isinstance(self.status_code, bool) or not isinstance(
            self.status_code, int
        ):
            raise TypeError("status_code must be an integer")
        if self.status_code != 429 and not 500 <= self.status_code <= 599:
            raise ValueError("status_code must be 429 or 5xx")


@dataclass(frozen=True, slots=True)
class InvalidResponse:
    reason: str

    def __post_init__(self) -> None:
        _text(self.reason, "reason")


@dataclass(frozen=True, slots=True)
class RequestRejected:
    status_code: int
    reason: str

    def __post_init__(self) -> None:
        if isinstance(self.status_code, bool) or not isinstance(
            self.status_code, int
        ):
            raise TypeError("status_code must be an integer")
        if not 400 <= self.status_code <= 499 or self.status_code in (404, 429):
            raise ValueError("status_code must be 4xx excluding 404 and 429")
        _text(self.reason, "reason")


CaseStateReadResult: TypeAlias = (
    Found
    | NotFound
    | TransportUnavailable
    | BackendUnavailable
    | InvalidResponse
    | RequestRejected
)
