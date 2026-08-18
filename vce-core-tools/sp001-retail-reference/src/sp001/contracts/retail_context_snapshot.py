from dataclasses import dataclass

from sp001.contracts.retail_context_dimension import (
    RetailContextDimension,
)


@dataclass(frozen=True, slots=True)
class RetailContextSnapshot:
    """Immutable, versioned retail context reference for an SP001 case."""

    snapshot_id: str
    snapshot_version: int
    case_id: str
    dimensions: tuple[RetailContextDimension, ...] = ()
