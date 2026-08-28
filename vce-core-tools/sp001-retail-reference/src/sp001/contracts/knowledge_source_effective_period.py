from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from sp001.contracts.knowledge_source_status import (
    KnowledgeSourceStatus,
)


class KnowledgeTemporalApplicabilityStatus(StrEnum):
    """Temporal position within one declared effective interval."""

    ACTIVE = "ACTIVE"
    NOT_YET_EFFECTIVE = "NOT_YET_EFFECTIVE"
    EXPIRED = "EXPIRED"


@dataclass(frozen=True, slots=True)
class KnowledgeSourceEffectivePeriod:
    """Half-open effective interval for one versioned source status."""

    source_status: KnowledgeSourceStatus
    effective_from: datetime
    effective_until: datetime | None = None

    def __post_init__(self) -> None:
        if not isinstance(
            self.source_status,
            KnowledgeSourceStatus,
        ):
            raise TypeError(
                "source_status must be a "
                "KnowledgeSourceStatus"
            )

        _validate_timezone_aware_datetime(
            field="effective_from",
            value=self.effective_from,
        )

        if self.effective_until is not None:
            _validate_timezone_aware_datetime(
                field="effective_until",
                value=self.effective_until,
            )

            if self.effective_until <= self.effective_from:
                raise ValueError(
                    "effective_until must be after effective_from"
                )


@dataclass(frozen=True, slots=True)
class KnowledgeSourceTemporalEvaluation:
    """Reproducible temporal evaluation without retrieval eligibility claims."""

    effective_period: KnowledgeSourceEffectivePeriod
    evaluated_at: datetime
    temporal_status: KnowledgeTemporalApplicabilityStatus

    def __post_init__(self) -> None:
        if not isinstance(
            self.effective_period,
            KnowledgeSourceEffectivePeriod,
        ):
            raise TypeError(
                "effective_period must be a "
                "KnowledgeSourceEffectivePeriod"
            )

        _validate_timezone_aware_datetime(
            field="evaluated_at",
            value=self.evaluated_at,
        )

        if not isinstance(
            self.temporal_status,
            KnowledgeTemporalApplicabilityStatus,
        ):
            raise TypeError(
                "temporal_status must be a "
                "KnowledgeTemporalApplicabilityStatus"
            )


def _validate_timezone_aware_datetime(
    *,
    field: str,
    value: object,
) -> None:
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
