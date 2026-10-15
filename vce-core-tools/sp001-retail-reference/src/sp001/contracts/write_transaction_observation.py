from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WriteTransactionObservation:
    """Durations in nanoseconds; excludes connection setup and signing."""

    operation: str
    begin_ns: int | None
    commit_ns: int | None
    rollback_ns: int | None
    total_ns: int
    committed: bool
    failed: bool
