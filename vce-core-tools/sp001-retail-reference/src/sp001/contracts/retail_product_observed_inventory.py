from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.retail_context_observation_provenance_binding import (
    RetailContextObservationProvenanceBinding,
)
from sp001.contracts.retail_context_scope import (
    RetailContextScope,
)
from sp001.contracts.retail_product_identity import (
    RetailProductIdentity,
)


class RetailInventoryQuantityUnit(StrEnum):
    """Closed unit vocabulary for observed retail inventory counts."""

    UNIT = "UNIT"


@dataclass(frozen=True, slots=True)
class RetailProductObservedInventory:
    """Immutable observed product quantity in one retail context."""

    product_identity: RetailProductIdentity
    context_scope: RetailContextScope
    observed_quantity: int
    quantity_unit: RetailInventoryQuantityUnit
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

        if (
            isinstance(
                self.observed_quantity,
                bool,
            )
            or not isinstance(
                self.observed_quantity,
                int,
            )
        ):
            raise TypeError(
                "observed_quantity must be an integer"
            )

        if self.observed_quantity < 0:
            raise ValueError(
                "observed_quantity must not be negative"
            )

        if not isinstance(
            self.quantity_unit,
            RetailInventoryQuantityUnit,
        ):
            raise TypeError(
                "quantity_unit must be a "
                "RetailInventoryQuantityUnit"
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
