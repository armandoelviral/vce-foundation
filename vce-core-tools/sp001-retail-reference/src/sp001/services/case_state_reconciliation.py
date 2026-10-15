from dataclasses import dataclass
from enum import StrEnum
from threading import RLock

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_state_read_result import (
    BackendUnavailable,
    CaseStateReadResult,
    Found,
    InvalidResponse,
    NotFound,
    RequestRejected,
    TransportUnavailable,
)


class ViewStatus(StrEnum):
    UNCONFIRMED = "UNCONFIRMED"
    CURRENT = "CURRENT"
    NOT_FOUND = "NOT_FOUND"
    UNAVAILABLE = "UNAVAILABLE"
    INVALID_RESPONSE = "INVALID_RESPONSE"
    REQUEST_REJECTED = "REQUEST_REJECTED"
    STALE_RESPONSE = "STALE_RESPONSE"
    READ_FAILED = "READ_FAILED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class ReadRequest:
    case_id: str
    sequence: int


@dataclass(frozen=True, slots=True)
class CaseView:
    case_id: str
    last_valid_state: CaseAuthoritativeState | None
    status: ViewStatus
    reason: str | None


class SessionResponseRejected(RuntimeError):
    """Control rejection without response payload."""


class CaseStateReconciler:
    """One case, latest-issued-request wins; no retries or storage writes."""

    def __init__(self, *, case_id: str) -> None:
        if not isinstance(case_id, str):
            raise TypeError("case_id must be a string")
        if not case_id.strip():
            raise ValueError("case_id must not be empty")
        self._case_id = case_id
        self._sequence = 0
        self._pending: ReadRequest | None = None
        self._terminated = False
        self._lock = RLock()
        self._view = CaseView(
            case_id, None, ViewStatus.UNCONFIRMED, None
        )

    @property
    def view(self) -> CaseView:
        with self._lock:
            return self._view

    def begin_read(self) -> ReadRequest:
        with self._lock:
            if self._terminated:
                raise SessionResponseRejected("session_terminated")
            self._sequence += 1
            self._pending = ReadRequest(self._case_id, self._sequence)
            self._set_view(ViewStatus.UNCONFIRMED, "read_pending")
            return self._pending

    def _set_view(self, status: ViewStatus, reason: str | None) -> None:
        self._view = CaseView(
            self._case_id, self._view.last_valid_state, status, reason
        )

    def fail_read(self, *, request: ReadRequest) -> bool:
        """Close the current request after an unclassified reader exception."""
        if not isinstance(request, ReadRequest):
            raise TypeError("request must be a ReadRequest")
        with self._lock:
            if request is not self._pending:
                return False
            self._pending = None
            self._set_view(ViewStatus.READ_FAILED, "reader_exception")
            return True

    def accept(
        self, *, request: ReadRequest, result: CaseStateReadResult
    ) -> bool:
        """Return False for superseded, foreign or consumed requests.

        True means the response was handled, not necessarily accepted as state.
        The exact request token returned by begin_read is required.
        """
        if not isinstance(request, ReadRequest):
            raise TypeError("request must be a ReadRequest")
        with self._lock:
            if self._terminated:
                raise SessionResponseRejected("session_terminated")
            if request is not self._pending:
                return False
            self._pending = None

            if isinstance(result, Found):
                incoming = result.state
                if incoming.case_id != self._case_id:
                    self._set_view(
                        ViewStatus.INVALID_RESPONSE, "case_id_mismatch"
                    )
                    return True

                current = self._view.last_valid_state
                if current is not None:
                    if incoming.revision < current.revision:
                        self._set_view(
                            ViewStatus.STALE_RESPONSE, "older_revision"
                        )
                        return True
                    if incoming.revision == current.revision:
                        if incoming != current:
                            self._set_view(
                                ViewStatus.INVALID_RESPONSE,
                                "same_revision_conflicting_state",
                            )
                            return True
                        self._set_view(ViewStatus.CURRENT, None)
                        return True

                self._view = CaseView(
                    self._case_id, incoming, ViewStatus.CURRENT, None
                )
            elif isinstance(result, NotFound):
                if result.case_id != self._case_id:
                    self._set_view(
                        ViewStatus.INVALID_RESPONSE, "case_id_mismatch"
                    )
                else:
                    self._set_view(ViewStatus.NOT_FOUND, None)
            elif isinstance(result, TransportUnavailable):
                self._set_view(ViewStatus.UNAVAILABLE, result.cause)
            elif isinstance(result, BackendUnavailable):
                self._set_view(
                    ViewStatus.UNAVAILABLE,
                    f"backend_status:{result.status_code}",
                )
            elif isinstance(result, InvalidResponse):
                self._set_view(ViewStatus.INVALID_RESPONSE, result.reason)
            elif isinstance(result, RequestRejected):
                self._set_view(
                    ViewStatus.REQUEST_REJECTED,
                    f"request_status:{result.status_code}:{result.reason}",
                )
            else:
                self._set_view(
                    ViewStatus.INVALID_RESPONSE, "unknown_read_result"
                )
            return True

    def terminate_session(self, *, reason: str) -> CaseView:
        """Withdraw owned snapshot and invalidate pending reads."""
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("reason must be nonempty")
        with self._lock:
            if not self._terminated:
                self._terminated = True
                self._pending = None
                self._view = CaseView(
                    self._case_id, None, ViewStatus.BLOCKED, reason,
                )
            return self._view
