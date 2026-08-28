from datetime import datetime

from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeSourceEffectivePeriod,
    KnowledgeSourceTemporalEvaluation,
    KnowledgeTemporalApplicabilityStatus,
)


def evaluate_knowledge_source_temporal_applicability(
    *,
    effective_period: KnowledgeSourceEffectivePeriod,
    evaluated_at: datetime,
) -> KnowledgeSourceTemporalEvaluation:
    """Evaluate an explicit instant against a half-open effective interval."""

    if not isinstance(
        effective_period,
        KnowledgeSourceEffectivePeriod,
    ):
        raise TypeError(
            "effective_period must be a "
            "KnowledgeSourceEffectivePeriod"
        )

    if not isinstance(
        evaluated_at,
        datetime,
    ):
        raise TypeError(
            "evaluated_at must be a datetime"
        )

    if (
        evaluated_at.tzinfo is None
        or evaluated_at.utcoffset() is None
    ):
        raise ValueError(
            "evaluated_at must be timezone-aware"
        )

    if evaluated_at < effective_period.effective_from:
        temporal_status = (
            KnowledgeTemporalApplicabilityStatus.NOT_YET_EFFECTIVE
        )
    elif (
        effective_period.effective_until is not None
        and evaluated_at >= effective_period.effective_until
    ):
        temporal_status = (
            KnowledgeTemporalApplicabilityStatus.EXPIRED
        )
    else:
        temporal_status = (
            KnowledgeTemporalApplicabilityStatus.ACTIVE
        )

    return KnowledgeSourceTemporalEvaluation(
        effective_period=effective_period,
        evaluated_at=evaluated_at,
        temporal_status=temporal_status,
    )
