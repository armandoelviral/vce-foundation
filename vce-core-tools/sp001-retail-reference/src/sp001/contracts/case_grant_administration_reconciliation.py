from dataclasses import dataclass
from enum import StrEnum


class AdministrationReconciliationStatus(StrEnum):
    """Observed administrative event reconciliation outcome."""

    EXACT_MATCH = "EXACT_MATCH"
    EVENT_CONFLICT = "EVENT_CONFLICT"
    EVENT_NOT_FOUND = "EVENT_NOT_FOUND"
    READ_UNAVAILABLE = "READ_UNAVAILABLE"
    READ_INVALID = "READ_INVALID"


@dataclass(frozen=True, slots=True)
class AdministrationReconciliationResult:
    """Immutable observation without authorization authority."""

    event_id: str
    status: AdministrationReconciliationStatus

    def __post_init__(self) -> None:
        if not isinstance(self.event_id, str):
            raise TypeError("event_id must be a string")

        if not self.event_id.strip():
            raise ValueError("event_id must not be empty")

        if not isinstance(
            self.status, AdministrationReconciliationStatus
        ):
            raise TypeError(
                "status must be an AdministrationReconciliationStatus"
            )
