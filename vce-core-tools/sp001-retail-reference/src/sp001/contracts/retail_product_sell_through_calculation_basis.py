from dataclasses import dataclass

from sp001.contracts.retail_product_observed_inventory import (
    RetailProductObservedInventory,
)
from sp001.contracts.retail_product_observed_sales_quantity import (
    RetailProductObservedSalesQuantity,
)


@dataclass(frozen=True, slots=True)
class RetailProductSellThroughCalculationBasis:
    """Declared observation inputs for one future sell-through calculation."""

    sales_observation: RetailProductObservedSalesQuantity
    inventory_observations: tuple[RetailProductObservedInventory, ...]
    calculation_scheme_id: str
    calculation_scheme_version: int

    def __post_init__(self) -> None:
        if not isinstance(
            self.sales_observation,
            RetailProductObservedSalesQuantity,
        ):
            raise TypeError(
                "sales_observation must be a "
                "RetailProductObservedSalesQuantity"
            )

        if not isinstance(self.inventory_observations, tuple):
            raise TypeError("inventory_observations must be a tuple")

        if not self.inventory_observations:
            raise ValueError(
                "inventory_observations must not be empty"
            )

        sales_product_identity = (
            self.sales_observation.product_identity
        )
        sales_context_scope = self.sales_observation.context_scope
        sales_quantity_unit = (
            self.sales_observation.quantity_unit.value
        )
        inventory_observation_identities: set[
            tuple[str, int]
        ] = set()

        for inventory_observation in self.inventory_observations:
            if not isinstance(
                inventory_observation,
                RetailProductObservedInventory,
            ):
                raise TypeError(
                    "inventory_observation must be a "
                    "RetailProductObservedInventory"
                )

            if (
                inventory_observation.product_identity
                != sales_product_identity
            ):
                raise ValueError(
                    "inventory observation product_identity must "
                    "match sales observation product_identity"
                )

            if (
                inventory_observation.context_scope
                != sales_context_scope
            ):
                raise ValueError(
                    "inventory observation context_scope must "
                    "match sales observation context_scope"
                )

            if (
                inventory_observation.quantity_unit.value
                != sales_quantity_unit
            ):
                raise ValueError(
                    "inventory and sales quantity units must match"
                )

            provenance = (
                inventory_observation
                .provenance_binding
                .provenance
            )
            observation_identity = (
                provenance.observation_id,
                provenance.observation_version,
            )

            if observation_identity in inventory_observation_identities:
                raise ValueError(
                    "duplicate inventory observation identity: "
                    f"{observation_identity[0]} "
                    f"version {observation_identity[1]}"
                )

            inventory_observation_identities.add(
                observation_identity
            )

        if not isinstance(self.calculation_scheme_id, str):
            raise TypeError("calculation_scheme_id must be a string")

        if not self.calculation_scheme_id:
            raise ValueError(
                "calculation_scheme_id must not be empty"
            )

        if (
            isinstance(self.calculation_scheme_version, bool)
            or not isinstance(self.calculation_scheme_version, int)
        ):
            raise TypeError(
                "calculation_scheme_version must be an integer"
            )

        if self.calculation_scheme_version <= 0:
            raise ValueError(
                "calculation_scheme_version must be positive"
            )
