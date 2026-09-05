from dataclasses import dataclass
from datetime import datetime

from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeTemporalApplicabilityStatus,
)
from sp001.contracts.retail_context_observation_provenance_binding import (
    RetailContextObservationProvenanceBinding,
)


@dataclass(frozen=True, slots=True)
class RetailContextObservationTemporalApplicabilityEvaluation:
    """Reproducible position within one observation effective interval."""

    binding: RetailContextObservationProvenanceBinding
    evaluated_at: datetime
    temporal_status: KnowledgeTemporalApplicabilityStatus

    def __post_init__(self) -> None:
        if not isinstance(
            self.binding,
            RetailContextObservationProvenanceBinding,
        ):
            raise TypeError(
                "binding must be a "
                "RetailContextObservationProvenanceBinding"
            )

        _validate_evaluated_at(
            self.evaluated_at,
        )

        if not isinstance(
            self.temporal_status,
            KnowledgeTemporalApplicabilityStatus,
        ):
            raise TypeError(
                "temporal_status must be a "
                "KnowledgeTemporalApplicabilityStatus"
            )

        expected_status = _temporal_status(
            binding=self.binding,
            evaluated_at=self.evaluated_at,
        )

        if self.temporal_status is not expected_status:
            raise ValueError(
                "temporal_status must match effective interval evaluation"
            )


def evaluate_retail_context_observation_temporal_applicability(
    *,
    binding: RetailContextObservationProvenanceBinding,
    evaluated_at: datetime,
) -> RetailContextObservationTemporalApplicabilityEvaluation:
    """Evaluate an explicit instant against the declared half-open interval."""

    if not isinstance(
        binding,
        RetailContextObservationProvenanceBinding,
    ):
        raise TypeError(
            "binding must be a "
            "RetailContextObservationProvenanceBinding"
        )

    _validate_evaluated_at(
        evaluated_at,
    )

    return RetailContextObservationTemporalApplicabilityEvaluation(
        binding=binding,
        evaluated_at=evaluated_at,
        temporal_status=_temporal_status(
            binding=binding,
            evaluated_at=evaluated_at,
        ),
    )


def _temporal_status(
    *,
    binding: RetailContextObservationProvenanceBinding,
    evaluated_at: datetime,
) -> KnowledgeTemporalApplicabilityStatus:
    provenance = binding.provenance

    if evaluated_at < provenance.effective_from:
        return KnowledgeTemporalApplicabilityStatus.NOT_YET_EFFECTIVE

    if (
        provenance.effective_until is not None
        and evaluated_at >= provenance.effective_until
    ):
        return KnowledgeTemporalApplicabilityStatus.EXPIRED

    return KnowledgeTemporalApplicabilityStatus.ACTIVE


def _validate_evaluated_at(
    value: object,
) -> None:
    if not isinstance(
        value,
        datetime,
    ):
        raise TypeError(
            "evaluated_at must be a datetime"
        )

    if (
        value.tzinfo is None
        or value.utcoffset() is None
    ):
        raise ValueError(
            "evaluated_at must be timezone-aware"
        )
