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

    def __post_init__(self) -> None:
        if (
            not isinstance(self.snapshot_id, str)
            or not self.snapshot_id.strip()
        ):
            raise ValueError("snapshot_id must not be empty")

        if (
            not isinstance(self.case_id, str)
            or not self.case_id.strip()
        ):
            raise ValueError("case_id must not be empty")

        if (
            isinstance(self.snapshot_version, bool)
            or not isinstance(self.snapshot_version, int)
            or self.snapshot_version < 1
        ):
            raise ValueError(
                "snapshot_version must be a positive integer"
            )

        if not isinstance(self.dimensions, tuple):
            raise TypeError(
                "dimensions must be an immutable tuple"
            )

        dimension_ids: set[str] = set()

        for dimension in self.dimensions:
            if not isinstance(
                dimension,
                RetailContextDimension,
            ):
                raise TypeError(
                    "every dimension must be a "
                    "RetailContextDimension"
                )

            if dimension.dimension_id in dimension_ids:
                raise ValueError(
                    "duplicate dimension_id: "
                    f"{dimension.dimension_id}"
                )

            dimension_ids.add(
                dimension.dimension_id
            )
