from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.retail_commercial_observation_period import (
    RetailCommercialObservationPeriod,
)
from sp001.contracts.retail_context_observation_provenance_binding import (
    RetailContextObservationProvenanceBinding,
)
from sp001.contracts.retail_context_scope import (
    RetailContextScope,
)
from sp001.contracts.retail_product_identity import (
    RetailProductIdentity,
)


class RetailCommercialQuantityUnit(StrEnum):
    """Closed unit vocabulary for observed commercial quantities."""

    UNIT = "UNIT"


@dataclass(frozen=True, slots=True)
class RetailProductObservedSalesQuantity:
    """Immutable observed product sales quantity for one closed period."""

    product_identity: RetailProductIdentity
    context_scope: RetailContextScope
    observation_period: RetailCommercialObservationPeriod
    sold_quantity: int
    quantity_unit: RetailCommercialQuantityUnit
    measurement_scheme_id: str
    measurement_scheme_version: int
    provenance_binding: RetailContextObservationProvenanceBinding

    def __post_init__(self) -> None:
        if not isinstance(
            self.product_identity,
            RetailProductIdentity,
        ):
            raise TypeError(
                "product_identity must be a RetailProductIdentity"
            )

        if not isinstance(
            self.context_scope,
            RetailContextScope,
        ):
            raise TypeError(
                "context_scope must be a RetailContextScope"
            )

        if not isinstance(
            self.observation_period,
            RetailCommercialObservationPeriod,
        ):
            raise TypeError(
                "observation_period must be a "
                "RetailCommercialObservationPeriod"
            )

        if (
            isinstance(
                self.sold_quantity,
                bool,
            )
            or not isinstance(
                self.sold_quantity,
                int,
            )
        ):
            raise TypeError(
                "sold_quantity must be an integer"
            )

        if self.sold_quantity < 0:
            raise ValueError(
                "sold_quantity must not be negative"
            )

        if not isinstance(
            self.quantity_unit,
            RetailCommercialQuantityUnit,
        ):
            raise TypeError(
                "quantity_unit must be a "
                "RetailCommercialQuantityUnit"
            )

        if (
            not isinstance(
                self.measurement_scheme_id,
                str,
            )
            or not self.measurement_scheme_id.strip()
        ):
            raise ValueError(
                "measurement_scheme_id must not be empty"
            )

        if (
            isinstance(
                self.measurement_scheme_version,
                bool,
            )
            or not isinstance(
                self.measurement_scheme_version,
                int,
            )
            or self.measurement_scheme_version < 1
        ):
            raise ValueError(
                "measurement_scheme_version must be a "
                "positive integer"
            )

        if not isinstance(
            self.provenance_binding,
            RetailContextObservationProvenanceBinding,
        ):
            raise TypeError(
                "provenance_binding must be a "
                "RetailContextObservationProvenanceBinding"
            )

        if (
            self.provenance_binding.snapshot.context_scope
            is not self.context_scope
        ):
            raise ValueError(
                "context_scope does not match provenance snapshot"
            )

        if (
            self.provenance_binding.provenance.observed_at
            < self.observation_period.period_until
        ):
            raise ValueError(
                "sales period must end no later than observed_at"
            )
