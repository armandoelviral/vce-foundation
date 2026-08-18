from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetailContextSnapshot:
    """Immutable, versioned retail context reference for an SP001 case."""

    snapshot_id: str
    snapshot_version: int
    case_id: str
