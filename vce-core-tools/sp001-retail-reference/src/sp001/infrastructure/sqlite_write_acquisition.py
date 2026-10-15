import sqlite3
from time import perf_counter_ns, sleep

from sp001.contracts.case_authoritative_state_store import (
    CaseWriteDeadlineExceeded,
)


class SpacedSqliteWriteAcquisition:
    """Acquire BEGIN IMMEDIATE with a deadline and spaced BUSY retries.

    Only acquisition is retried. The caller owns mutations, commit, rollback
    and the post-acquisition deadline check. No fairness guarantee.
    The dedicated connection keeps busy_timeout=0 until it is closed.
    """

    def __init__(
        self, *, pause_ns: int, clock=perf_counter_ns, wait=sleep,
    ):
        if type(pause_ns) is not int:
            raise TypeError("pause_ns must be an integer")
        if pause_ns <= 0:
            raise ValueError("pause_ns must be positive")
        if not callable(clock) or not callable(wait):
            raise TypeError("clock and wait must be callable")
        self._pause_ns = pause_ns
        self._clock = clock
        self._wait = wait

    def begin(self, connection, *, deadline_ns: int):
        if type(deadline_ns) is not int:
            raise TypeError("deadline_ns must be an integer")
        if deadline_ns < 0:
            raise ValueError("deadline_ns must be nonnegative")
        if connection.in_transaction:
            raise RuntimeError("write acquisition requires no active transaction")
        if self._clock() >= deadline_ns:
            raise CaseWriteDeadlineExceeded("case_write_deadline_exceeded")
        connection.execute("PRAGMA busy_timeout=0")
        while True:
            if self._clock() >= deadline_ns:
                raise CaseWriteDeadlineExceeded("case_write_deadline_exceeded")
            try:
                return connection.execute("BEGIN IMMEDIATE")
            except sqlite3.OperationalError as error:
                code = getattr(error, "sqlite_errorcode", None)
                if (
                    code is None
                    or (code & 0xff) != sqlite3.SQLITE_BUSY
                    or connection.in_transaction
                ):
                    raise
                remaining = deadline_ns - self._clock()
                if remaining <= 0:
                    raise CaseWriteDeadlineExceeded(
                        "case_write_deadline_exceeded"
                    ) from error
                self._wait(min(self._pause_ns, remaining) / 1_000_000_000)
