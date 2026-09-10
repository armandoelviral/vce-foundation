from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class RetailCommercialObservationPeriod:
    """Immutable half-open period for one commercial observation."""

    period_id: str
    period_version: int
    period_from: datetime
    period_until: datetime

    def __post_init__(self) -> None:
        if (
            not isinstance(
                self.period_id,
                str,
            )
            or not self.period_id.strip()
        ):
            raise ValueError(
                "period_id must not be empty"
            )

        if (
            isinstance(
                self.period_version,
                bool,
            )
            or not isinstance(
                self.period_version,
                int,
            )
            or self.period_version < 1
        ):
            raise ValueError(
                "period_version must be a positive integer"
            )

        temporal_fields = {
            "period_from": self.period_from,
            "period_until": self.period_until,
        }

        for field, value in temporal_fields.items():
            if not isinstance(
                value,
                datetime,
            ):
                raise TypeError(
                    f"{field} must be a datetime"
                )

            if (
                value.tzinfo is None
                or value.utcoffset() is None
            ):
                raise ValueError(
                    f"{field} must be timezone-aware"
                )

        if self.period_until <= self.period_from:
            raise ValueError(
                "period_until must be after period_from"
            )
