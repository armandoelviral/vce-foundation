from enum import StrEnum

from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)


class DimensionEvaluationStatus(StrEnum):
    """Evaluation availability for one retail context dimension."""

    EVALUABLE = "EVALUABLE"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    OPTIONAL_UNAVAILABLE = "OPTIONAL_UNAVAILABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    DISPUTED = "DISPUTED"


def evaluate_context_dimension(
    dimension: RetailContextDimension,
) -> DimensionEvaluationStatus:
    """Determine whether a dimension can support its evaluation."""

    if not isinstance(
        dimension,
        RetailContextDimension,
    ):
        raise TypeError(
            "dimension must be a RetailContextDimension"
        )

    if (
        dimension.applicability
        is DimensionApplicability.DISPUTED
        or dimension.evidence_status
        is DimensionEvidenceStatus.DISPUTED
    ):
        return DimensionEvaluationStatus.DISPUTED

    if (
        dimension.applicability
        is DimensionApplicability.NOT_APPLICABLE
    ):
        return DimensionEvaluationStatus.NOT_APPLICABLE

    unavailable_evidence = {
        DimensionEvidenceStatus.NOT_PROVIDED,
        DimensionEvidenceStatus.INSUFFICIENT_EVIDENCE,
    }

    if dimension.evidence_status in unavailable_evidence:
        if (
            dimension.applicability
            is DimensionApplicability.OPTIONAL
        ):
            return (
                DimensionEvaluationStatus.OPTIONAL_UNAVAILABLE
            )

        return (
            DimensionEvaluationStatus.INSUFFICIENT_EVIDENCE
        )

    return DimensionEvaluationStatus.EVALUABLE
