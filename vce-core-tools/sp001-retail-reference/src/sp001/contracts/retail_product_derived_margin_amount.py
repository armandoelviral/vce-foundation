from dataclasses import dataclass
from datetime import datetime

from sp001.contracts.retail_commercial_monetary_amount import (
    RetailCommercialMonetaryAmount,
)
from sp001.contracts.retail_product_margin_calculation_basis import (
    RetailProductMarginCalculationBasis,
)


@dataclass(frozen=True, slots=True)
class RetailProductDerivedMarginAmount:
    """Exact signed monetary margin for one declared calculation basis."""

    result_id: str
    result_version: int
    calculation_basis: RetailProductMarginCalculationBasis
    margin_amount: RetailCommercialMonetaryAmount
    derived_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.result_id, str):
            raise TypeError("result_id must be a string")

        if not self.result_id:
            raise ValueError("result_id must not be empty")

        if (
            isinstance(self.result_version, bool)
            or not isinstance(self.result_version, int)
        ):
            raise TypeError("result_version must be an integer")

        if self.result_version <= 0:
            raise ValueError("result_version must be positive")

        if not isinstance(
            self.calculation_basis,
            RetailProductMarginCalculationBasis,
        ):
            raise TypeError(
                "calculation_basis must be a "
                "RetailProductMarginCalculationBasis"
            )

        if not isinstance(
            self.margin_amount,
            RetailCommercialMonetaryAmount,
        ):
            raise TypeError(
                "margin_amount must be a "
                "RetailCommercialMonetaryAmount"
            )

        basis_currency_identity = (
            self.calculation_basis
            .price_observation
            .monetary_amount
            .currency_identity
        )

        if (
            self.margin_amount.currency_identity
            != basis_currency_identity
        ):
            raise ValueError(
                "margin_amount currency_identity must match "
                "calculation basis currency_identity"
            )

        if not isinstance(self.derived_at, datetime):
            raise TypeError("derived_at must be a datetime")

        if (
            self.derived_at.tzinfo is None
            or self.derived_at.utcoffset() is None
        ):
            raise ValueError("derived_at must be timezone-aware")
