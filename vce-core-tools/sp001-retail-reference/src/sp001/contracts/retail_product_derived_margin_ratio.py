from dataclasses import dataclass
from datetime import datetime
from math import gcd

from sp001.contracts.retail_product_margin_calculation_basis import (
    RetailProductMarginCalculationBasis,
)


@dataclass(frozen=True, slots=True)
class RetailProductDerivedMarginRatio:
    """Canonical exact signed ratio for one declared margin basis."""

    result_id: str
    result_version: int
    calculation_basis: RetailProductMarginCalculationBasis
    numerator: int
    denominator: int
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

        if (
            isinstance(self.numerator, bool)
            or not isinstance(self.numerator, int)
        ):
            raise TypeError("numerator must be an integer")

        if (
            isinstance(self.denominator, bool)
            or not isinstance(self.denominator, int)
        ):
            raise TypeError("denominator must be an integer")

        if self.denominator <= 0:
            raise ValueError("denominator must be positive")

        if gcd(self.numerator, self.denominator) != 1:
            raise ValueError(
                "numerator and denominator must form a canonical "
                "irreducible ratio"
            )

        if not isinstance(self.derived_at, datetime):
            raise TypeError("derived_at must be a datetime")

        if (
            self.derived_at.tzinfo is None
            or self.derived_at.utcoffset() is None
        ):
            raise ValueError("derived_at must be timezone-aware")
