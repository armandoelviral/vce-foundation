from dataclasses import dataclass

from sp001.contracts.retail_context_dimension import (
    RetailContextDimension,
)
from sp001.contracts.retail_context_observation_provenance import (
    RetailContextObservationProvenance,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)


@dataclass(frozen=True, slots=True)
class RetailContextObservationProvenanceBinding:
    """Immutable binding of temporal provenance to one snapshot dimension."""

    snapshot: RetailContextSnapshot
    dimension: RetailContextDimension
    provenance: RetailContextObservationProvenance

    def __post_init__(self) -> None:
        if not isinstance(
            self.snapshot,
            RetailContextSnapshot,
        ):
            raise TypeError(
                "snapshot must be a RetailContextSnapshot"
            )

        if not isinstance(
            self.dimension,
            RetailContextDimension,
        ):
            raise TypeError(
                "dimension must be a RetailContextDimension"
            )

        if not isinstance(
            self.provenance,
            RetailContextObservationProvenance,
        ):
            raise TypeError(
                "provenance must be a "
                "RetailContextObservationProvenance"
            )

        if self.provenance.case_id != self.snapshot.case_id:
            raise ValueError(
                "provenance case_id does not match snapshot"
            )

        if (
            self.provenance.snapshot_id
            != self.snapshot.snapshot_id
        ):
            raise ValueError(
                "provenance snapshot_id does not match snapshot"
            )

        if (
            self.provenance.snapshot_version
            != self.snapshot.snapshot_version
        ):
            raise ValueError(
                "provenance snapshot_version does not match snapshot"
            )

        if (
            self.provenance.dimension_id
            != self.dimension.dimension_id
        ):
            raise ValueError(
                "provenance dimension_id does not match dimension"
            )

        if not any(
            candidate is self.dimension
            for candidate in self.snapshot.dimensions
        ):
            raise ValueError(
                "dimension must belong to snapshot"
            )


def bind_retail_context_observation_provenance(
    *,
    snapshot: RetailContextSnapshot,
    provenance: RetailContextObservationProvenance,
) -> RetailContextObservationProvenanceBinding:
    """Bind provenance to its exact declared snapshot dimension."""

    if not isinstance(
        snapshot,
        RetailContextSnapshot,
    ):
        raise TypeError(
            "snapshot must be a RetailContextSnapshot"
        )

    if not isinstance(
        provenance,
        RetailContextObservationProvenance,
    ):
        raise TypeError(
            "provenance must be a "
            "RetailContextObservationProvenance"
        )

    if provenance.case_id != snapshot.case_id:
        raise ValueError(
            "provenance case_id does not match snapshot"
        )

    if provenance.snapshot_id != snapshot.snapshot_id:
        raise ValueError(
            "provenance snapshot_id does not match snapshot"
        )

    if (
        provenance.snapshot_version
        != snapshot.snapshot_version
    ):
        raise ValueError(
            "provenance snapshot_version does not match snapshot"
        )

    dimension = next(
        (
            candidate
            for candidate in snapshot.dimensions
            if (
                candidate.dimension_id
                == provenance.dimension_id
            )
        ),
        None,
    )

    if dimension is None:
        raise ValueError(
            "provenance dimension_id not present in snapshot: "
            f"{provenance.dimension_id}"
        )

    return RetailContextObservationProvenanceBinding(
        snapshot=snapshot,
        dimension=dimension,
        provenance=provenance,
    )
