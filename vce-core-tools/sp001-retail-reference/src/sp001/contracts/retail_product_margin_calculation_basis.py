from dataclasses import dataclass

from sp001.contracts.retail_product_observed_cost import (
    RetailProductObservedCost,
)
from sp001.contracts.retail_product_observed_price import (
    RetailProductObservedPrice,
)


@dataclass(frozen=True, slots=True)
class RetailProductMarginCalculationBasis:
    """Declared price and cost inputs for one future margin calculation."""

    price_observation: RetailProductObservedPrice
    cost_observation: RetailProductObservedCost
    calculation_scheme_id: str
    calculation_scheme_version: int

    def __post_init__(self) -> None:
        if not isinstance(
            self.price_observation,
            RetailProductObservedPrice,
        ):
            raise TypeError(
                "price_observation must be a "
                "RetailProductObservedPrice"
            )

        if not isinstance(
            self.cost_observation,
            RetailProductObservedCost,
        ):
            raise TypeError(
                "cost_observation must be a "
                "RetailProductObservedCost"
            )

        if (
            self.cost_observation.product_identity
            != self.price_observation.product_identity
        ):
            raise ValueError(
                "cost observation product_identity must match "
                "price observation product_identity"
            )

        if (
            self.cost_observation.context_scope
            != self.price_observation.context_scope
        ):
            raise ValueError(
                "cost observation context_scope must match "
                "price observation context_scope"
            )

        price_currency_identity = (
            self.price_observation
            .monetary_amount
            .currency_identity
        )
        cost_currency_identity = (
            self.cost_observation
            .monetary_amount
            .currency_identity
        )

        if cost_currency_identity != price_currency_identity:
            raise ValueError(
                "cost observation currency_identity must match "
                "price observation currency_identity"
            )

        if not isinstance(self.calculation_scheme_id, str):
            raise TypeError(
                "calculation_scheme_id must be a string"
            )

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
