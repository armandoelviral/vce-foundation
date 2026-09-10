from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from sp001.contracts.retail_product_margin_calculation_basis import (
    RetailProductMarginCalculationBasis,
)


class RetailProductMarginRatioIndeterminacyReason(StrEnum):
    """Closed reasons why one declared basis produced no margin ratio."""

    UNSUPPORTED_CALCULATION_SCHEME = (
        "UNSUPPORTED_CALCULATION_SCHEME"
    )
    INSUFFICIENT_INPUT_EVIDENCE = "INSUFFICIENT_INPUT_EVIDENCE"
    NONPOSITIVE_DENOMINATOR = "NONPOSITIVE_DENOMINATOR"


@dataclass(frozen=True, slots=True)
class RetailProductIndeterminateMarginRatioResult:
    """Typed absence of a margin ratio for one calculation basis."""

    result_id: str
    result_version: int
    calculation_basis: RetailProductMarginCalculationBasis
    reason: RetailProductMarginRatioIndeterminacyReason
    determined_at: datetime

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
            self.reason,
            RetailProductMarginRatioIndeterminacyReason,
        ):
            raise TypeError(
                "reason must be a "
                "RetailProductMarginRatioIndeterminacyReason"
            )
        if not isinstance(self.determined_at, datetime):
            raise TypeError("determined_at must be a datetime")
        if (
            self.determined_at.tzinfo is None
            or self.determined_at.utcoffset() is None
        ):
            raise ValueError("determined_at must be timezone-aware")
