from dataclasses import dataclass

from sp001.contracts.retail_commercial_currency_identity import (
    RetailCommercialCurrencyIdentity,
)


@dataclass(frozen=True, slots=True)
class RetailCommercialMonetaryAmount:
    """Exact signed count of scheme-defined currency minor units."""

    currency_identity: RetailCommercialCurrencyIdentity
    minor_unit_amount: int

    def __post_init__(self) -> None:
        if not isinstance(
            self.currency_identity,
            RetailCommercialCurrencyIdentity,
        ):
            raise TypeError(
                "currency_identity must be a "
                "RetailCommercialCurrencyIdentity"
            )

        if (
            isinstance(self.minor_unit_amount, bool)
            or not isinstance(self.minor_unit_amount, int)
        ):
            raise TypeError("minor_unit_amount must be an integer")
