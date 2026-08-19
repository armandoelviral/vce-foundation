from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)
from sp001.contracts.retail_context_dimension_evaluation import (
    DimensionEvaluationStatus,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)
from sp001.contracts.retail_context_snapshot_evaluation import (
    SnapshotEvaluationStatus,
    evaluate_context_snapshot,
)


def build_dimension(
    *,
    dimension_id: str,
    applicability: DimensionApplicability,
    evidence_status: DimensionEvidenceStatus,
    value: str | None = None,
) -> RetailContextDimension:
    return RetailContextDimension(
        dimension_id=dimension_id,
        dimension_type="CUSTOMER_DEFINED_DIMENSION",
        applicability=applicability,
        evidence_status=evidence_status,
        value=value,
    )


def build_snapshot(
    *dimensions: RetailContextDimension,
) -> RetailContextSnapshot:
    return RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
        dimensions=dimensions,
    )


def test_empty_snapshot_is_not_declared_commercially_evaluable() -> None:
    result = evaluate_context_snapshot(
        build_snapshot(),
    )

    assert result.status is SnapshotEvaluationStatus.NO_DIMENSIONS
    assert result.dimension_results == ()


def test_required_documented_dimension_makes_snapshot_evaluable() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    result = evaluate_context_snapshot(
        build_snapshot(department),
    )

    assert result.status is SnapshotEvaluationStatus.EVALUABLE

    assert result.dimension_results == (
        (
            "CTX-DEPARTMENT-001",
            DimensionEvaluationStatus.EVALUABLE,
        ),
    )


def test_missing_required_dimension_blocks_snapshot() -> None:
    capacity = build_dimension(
        dimension_id="CTX-CAPACITY-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    result = evaluate_context_snapshot(
        build_snapshot(capacity),
    )

    assert (
        result.status
        is SnapshotEvaluationStatus.INSUFFICIENT_EVIDENCE
    )

    assert result.dimension_results == (
        (
            "CTX-CAPACITY-001",
            DimensionEvaluationStatus.INSUFFICIENT_EVIDENCE,
        ),
    )


def test_optional_missing_dimension_does_not_block_snapshot() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    cluster = build_dimension(
        dimension_id="CTX-CLUSTER-001",
        applicability=DimensionApplicability.OPTIONAL,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    result = evaluate_context_snapshot(
        build_snapshot(department, cluster),
    )

    assert result.status is SnapshotEvaluationStatus.EVALUABLE

    assert result.dimension_results == (
        (
            "CTX-DEPARTMENT-001",
            DimensionEvaluationStatus.EVALUABLE,
        ),
        (
            "CTX-CLUSTER-001",
            DimensionEvaluationStatus.OPTIONAL_UNAVAILABLE,
        ),
    )


def test_not_applicable_dimension_does_not_block_snapshot() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    cluster = build_dimension(
        dimension_id="CTX-CLUSTER-001",
        applicability=DimensionApplicability.NOT_APPLICABLE,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    result = evaluate_context_snapshot(
        build_snapshot(department, cluster),
    )

    assert result.status is SnapshotEvaluationStatus.EVALUABLE

    assert result.dimension_results == (
        (
            "CTX-DEPARTMENT-001",
            DimensionEvaluationStatus.EVALUABLE,
        ),
        (
            "CTX-CLUSTER-001",
            DimensionEvaluationStatus.NOT_APPLICABLE,
        ),
    )


def test_disputed_dimension_blocks_full_context_validation() -> None:
    context = build_dimension(
        dimension_id="CTX-CONTEXT-001",
        applicability=DimensionApplicability.DISPUTED,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value="DECLARED_CONTEXT_UNVERIFIED",
    )

    result = evaluate_context_snapshot(
        build_snapshot(context),
    )

    assert result.status is SnapshotEvaluationStatus.DISPUTED

    assert result.dimension_results == (
        (
            "CTX-CONTEXT-001",
            DimensionEvaluationStatus.DISPUTED,
        ),
    )


def test_dispute_takes_priority_over_missing_required_evidence() -> None:
    capacity = build_dimension(
        dimension_id="CTX-CAPACITY-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    context = build_dimension(
        dimension_id="CTX-CONTEXT-001",
        applicability=DimensionApplicability.DISPUTED,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value="DECLARED_CONTEXT_UNVERIFIED",
    )

    result = evaluate_context_snapshot(
        build_snapshot(capacity, context),
    )

    assert result.status is SnapshotEvaluationStatus.DISPUTED

    assert result.dimension_results == (
        (
            "CTX-CAPACITY-001",
            DimensionEvaluationStatus.INSUFFICIENT_EVIDENCE,
        ),
        (
            "CTX-CONTEXT-001",
            DimensionEvaluationStatus.DISPUTED,
        ),
    )


def test_snapshot_evaluation_preserves_snapshot_identity() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    result = evaluate_context_snapshot(
        build_snapshot(department),
    )

    assert result.snapshot_id == "RCP-SNAPSHOT-001"
    assert result.snapshot_version == 1
    assert result.case_id == "CASE-001"


def test_snapshot_evaluation_preserves_dimension_order() -> None:
    first = build_dimension(
        dimension_id="CTX-FIXTURE-002",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="BACKWALL",
    )

    second = build_dimension(
        dimension_id="CTX-FIXTURE-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="GONDOLA",
    )

    result = evaluate_context_snapshot(
        build_snapshot(first, second),
    )

    assert tuple(
        dimension_id
        for dimension_id, _ in result.dimension_results
    ) == (
        "CTX-FIXTURE-002",
        "CTX-FIXTURE-001",
    )


def test_snapshot_evaluation_result_is_immutable() -> None:
    result = evaluate_context_snapshot(
        build_snapshot(),
    )

    with pytest.raises(FrozenInstanceError):
        result.case_id = "CASE-002"


def test_snapshot_evaluation_rejects_invalid_input() -> None:
    with pytest.raises(
        TypeError,
        match="snapshot must be a RetailContextSnapshot",
    ):
        evaluate_context_snapshot(
            "RCP-SNAPSHOT-001",
        )


def test_snapshot_evaluation_vocabulary_is_exact() -> None:
    assert {
        state.value
        for state in SnapshotEvaluationStatus
    } == {
        "EVALUABLE",
        "INSUFFICIENT_EVIDENCE",
        "DISPUTED",
        "NO_DIMENSIONS",
    }
