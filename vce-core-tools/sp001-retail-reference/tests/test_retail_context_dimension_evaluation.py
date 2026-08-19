import pytest

from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)
from sp001.contracts.retail_context_dimension_evaluation import (
    DimensionEvaluationStatus,
    evaluate_context_dimension,
)


def build_dimension(
    *,
    applicability: DimensionApplicability,
    evidence_status: DimensionEvidenceStatus,
    value: str | None = None,
) -> RetailContextDimension:
    return RetailContextDimension(
        dimension_id="CTX-FIXTURE-001",
        dimension_type="FIXTURE_TYPE",
        applicability=applicability,
        evidence_status=evidence_status,
        value=value,
    )


@pytest.mark.parametrize(
    "evidence_status",
    (
        DimensionEvidenceStatus.DOCUMENTED,
        DimensionEvidenceStatus.HUMAN_DECLARED,
        DimensionEvidenceStatus.MEASURED,
        DimensionEvidenceStatus.INDEPENDENTLY_VERIFIED,
    ),
)
def test_required_dimension_with_supported_value_is_evaluable(
    evidence_status: DimensionEvidenceStatus,
) -> None:
    dimension = build_dimension(
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=evidence_status,
        value="BACKWALL",
    )

    assert (
        evaluate_context_dimension(dimension)
        is DimensionEvaluationStatus.EVALUABLE
    )


def test_required_dimension_without_evidence_is_insufficient() -> None:
    dimension = build_dimension(
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    assert (
        evaluate_context_dimension(dimension)
        is DimensionEvaluationStatus.INSUFFICIENT_EVIDENCE
    )


def test_required_dimension_with_partial_evidence_is_insufficient() -> None:
    dimension = build_dimension(
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=(
            DimensionEvidenceStatus.INSUFFICIENT_EVIDENCE
        ),
        value="UNVERIFIED_FIXTURE",
    )

    assert (
        evaluate_context_dimension(dimension)
        is DimensionEvaluationStatus.INSUFFICIENT_EVIDENCE
    )


def test_optional_dimension_without_evidence_does_not_block() -> None:
    dimension = build_dimension(
        applicability=DimensionApplicability.OPTIONAL,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    assert (
        evaluate_context_dimension(dimension)
        is DimensionEvaluationStatus.OPTIONAL_UNAVAILABLE
    )


def test_optional_dimension_with_supported_value_is_evaluable() -> None:
    dimension = build_dimension(
        applicability=DimensionApplicability.OPTIONAL,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="BACKWALL",
    )

    assert (
        evaluate_context_dimension(dimension)
        is DimensionEvaluationStatus.EVALUABLE
    )


def test_not_applicable_dimension_does_not_block() -> None:
    dimension = build_dimension(
        applicability=DimensionApplicability.NOT_APPLICABLE,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    assert (
        evaluate_context_dimension(dimension)
        is DimensionEvaluationStatus.NOT_APPLICABLE
    )


def test_disputed_applicability_remains_disputed() -> None:
    dimension = build_dimension(
        applicability=DimensionApplicability.DISPUTED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CONTESTED_CONTEXT",
    )

    assert (
        evaluate_context_dimension(dimension)
        is DimensionEvaluationStatus.DISPUTED
    )


def test_disputed_evidence_remains_disputed() -> None:
    dimension = build_dimension(
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value="CONTESTED_CONTEXT",
    )

    assert (
        evaluate_context_dimension(dimension)
        is DimensionEvaluationStatus.DISPUTED
    )


def test_optional_disputed_evidence_remains_disputed() -> None:
    dimension = build_dimension(
        applicability=DimensionApplicability.OPTIONAL,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value="CONTESTED_CONTEXT",
    )

    assert (
        evaluate_context_dimension(dimension)
        is DimensionEvaluationStatus.DISPUTED
    )


def test_optional_partial_evidence_does_not_block() -> None:
    dimension = build_dimension(
        applicability=DimensionApplicability.OPTIONAL,
        evidence_status=(
            DimensionEvidenceStatus.INSUFFICIENT_EVIDENCE
        ),
        value="UNVERIFIED_FIXTURE",
    )

    assert (
        evaluate_context_dimension(dimension)
        is DimensionEvaluationStatus.OPTIONAL_UNAVAILABLE
    )


def test_evaluation_rejects_non_dimension_input() -> None:
    with pytest.raises(
        TypeError,
        match="dimension must be a RetailContextDimension",
    ):
        evaluate_context_dimension("CTX-FIXTURE-001")


def test_evaluation_vocabulary_is_exact() -> None:
    assert {
        status.value
        for status in DimensionEvaluationStatus
    } == {
        "EVALUABLE",
        "INSUFFICIENT_EVIDENCE",
        "OPTIONAL_UNAVAILABLE",
        "NOT_APPLICABLE",
        "DISPUTED",
    }
