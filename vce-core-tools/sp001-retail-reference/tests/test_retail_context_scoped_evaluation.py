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
from sp001.contracts.retail_context_scoped_evaluation import (
    ScopedEvaluationStatus,
    evaluate_context_scope,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
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


def test_scope_with_supported_dimension_is_evaluable() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    result = evaluate_context_scope(
        build_snapshot(department),
        required_dimension_ids=("CTX-DEPARTMENT-001",),
    )

    assert result.status is ScopedEvaluationStatus.EVALUABLE

    assert result.dimension_results == (
        (
            "CTX-DEPARTMENT-001",
            DimensionEvaluationStatus.EVALUABLE,
        ),
    )


def test_unrelated_missing_dimension_does_not_block_scope() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    capacity = build_dimension(
        dimension_id="CTX-CAPACITY-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    result = evaluate_context_scope(
        build_snapshot(department, capacity),
        required_dimension_ids=("CTX-DEPARTMENT-001",),
    )

    assert result.status is ScopedEvaluationStatus.EVALUABLE

    assert result.dimension_results == (
        (
            "CTX-DEPARTMENT-001",
            DimensionEvaluationStatus.EVALUABLE,
        ),
    )


def test_unrelated_disputed_dimension_does_not_block_scope() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    context = build_dimension(
        dimension_id="CTX-CONTEXT-001",
        applicability=DimensionApplicability.DISPUTED,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value="DECLARED_CONTEXT_UNVERIFIED",
    )

    result = evaluate_context_scope(
        build_snapshot(department, context),
        required_dimension_ids=("CTX-DEPARTMENT-001",),
    )

    assert result.status is ScopedEvaluationStatus.EVALUABLE

    assert result.dimension_results == (
        (
            "CTX-DEPARTMENT-001",
            DimensionEvaluationStatus.EVALUABLE,
        ),
    )


def test_required_dimension_missing_from_snapshot_is_insufficient() -> None:
    result = evaluate_context_scope(
        build_snapshot(),
        required_dimension_ids=("CTX-CAPACITY-001",),
    )

    assert (
        result.status
        is ScopedEvaluationStatus.INSUFFICIENT_EVIDENCE
    )

    assert result.missing_dimension_ids == (
        "CTX-CAPACITY-001",
    )

    assert result.dimension_results == ()


def test_required_dimension_without_evidence_is_insufficient() -> None:
    capacity = build_dimension(
        dimension_id="CTX-CAPACITY-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    result = evaluate_context_scope(
        build_snapshot(capacity),
        required_dimension_ids=("CTX-CAPACITY-001",),
    )

    assert (
        result.status
        is ScopedEvaluationStatus.INSUFFICIENT_EVIDENCE
    )

    assert result.dimension_results == (
        (
            "CTX-CAPACITY-001",
            DimensionEvaluationStatus.INSUFFICIENT_EVIDENCE,
        ),
    )


def test_required_disputed_dimension_keeps_scope_disputed() -> None:
    context = build_dimension(
        dimension_id="CTX-CONTEXT-001",
        applicability=DimensionApplicability.DISPUTED,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value="DECLARED_CONTEXT_UNVERIFIED",
    )

    result = evaluate_context_scope(
        build_snapshot(context),
        required_dimension_ids=("CTX-CONTEXT-001",),
    )

    assert result.status is ScopedEvaluationStatus.DISPUTED


def test_disputed_required_dimension_takes_priority() -> None:
    context = build_dimension(
        dimension_id="CTX-CONTEXT-001",
        applicability=DimensionApplicability.DISPUTED,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value="DECLARED_CONTEXT_UNVERIFIED",
    )

    result = evaluate_context_scope(
        build_snapshot(context),
        required_dimension_ids=(
            "CTX-CONTEXT-001",
            "CTX-CAPACITY-001",
        ),
    )

    assert result.status is ScopedEvaluationStatus.DISPUTED

    assert result.missing_dimension_ids == (
        "CTX-CAPACITY-001",
    )


def test_required_not_applicable_dimension_cannot_support_scope() -> None:
    cluster = build_dimension(
        dimension_id="CTX-CLUSTER-001",
        applicability=DimensionApplicability.NOT_APPLICABLE,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    result = evaluate_context_scope(
        build_snapshot(cluster),
        required_dimension_ids=("CTX-CLUSTER-001",),
    )

    assert (
        result.status
        is ScopedEvaluationStatus.INSUFFICIENT_EVIDENCE
    )

    assert result.dimension_results == (
        (
            "CTX-CLUSTER-001",
            DimensionEvaluationStatus.NOT_APPLICABLE,
        ),
    )


def test_required_optional_unavailable_dimension_cannot_support_scope() -> None:
    cluster = build_dimension(
        dimension_id="CTX-CLUSTER-001",
        applicability=DimensionApplicability.OPTIONAL,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    result = evaluate_context_scope(
        build_snapshot(cluster),
        required_dimension_ids=("CTX-CLUSTER-001",),
    )

    assert (
        result.status
        is ScopedEvaluationStatus.INSUFFICIENT_EVIDENCE
    )

    assert result.dimension_results == (
        (
            "CTX-CLUSTER-001",
            DimensionEvaluationStatus.OPTIONAL_UNAVAILABLE,
        ),
    )


def test_scope_preserves_declared_requirement_order() -> None:
    first = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    second = build_dimension(
        dimension_id="CTX-FIXTURE-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="BACKWALL",
    )

    result = evaluate_context_scope(
        build_snapshot(first, second),
        required_dimension_ids=(
            "CTX-FIXTURE-001",
            "CTX-DEPARTMENT-001",
        ),
    )

    assert tuple(
        dimension_id
        for dimension_id, _ in result.dimension_results
    ) == (
        "CTX-FIXTURE-001",
        "CTX-DEPARTMENT-001",
    )


def test_scope_preserves_snapshot_identity() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    result = evaluate_context_scope(
        build_snapshot(department),
        required_dimension_ids=("CTX-DEPARTMENT-001",),
    )

    assert result.snapshot_id == "RCP-SNAPSHOT-001"
    assert result.snapshot_version == 1
    assert result.case_id == "CASE-001"


def test_scope_result_is_immutable() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    result = evaluate_context_scope(
        build_snapshot(department),
        required_dimension_ids=("CTX-DEPARTMENT-001",),
    )

    with pytest.raises(FrozenInstanceError):
        result.case_id = "CASE-002"


def test_scope_rejects_non_snapshot_input() -> None:
    with pytest.raises(
        TypeError,
        match="snapshot must be a RetailContextSnapshot",
    ):
        evaluate_context_scope(
            "RCP-SNAPSHOT-001",
            required_dimension_ids=("CTX-DEPARTMENT-001",),
        )


def test_scope_rejects_mutable_requirement_collection() -> None:
    with pytest.raises(
        TypeError,
        match="required_dimension_ids must be an immutable tuple",
    ):
        evaluate_context_scope(
            build_snapshot(),
            required_dimension_ids=["CTX-DEPARTMENT-001"],
        )


def test_scope_rejects_empty_requirement_collection() -> None:
    with pytest.raises(
        ValueError,
        match="required_dimension_ids must not be empty",
    ):
        evaluate_context_scope(
            build_snapshot(),
            required_dimension_ids=(),
        )


def test_scope_rejects_blank_requirement_identity() -> None:
    with pytest.raises(
        ValueError,
        match="required dimension_id must not be empty",
    ):
        evaluate_context_scope(
            build_snapshot(),
            required_dimension_ids=("   ",),
        )


def test_scope_rejects_non_string_requirement_identity() -> None:
    with pytest.raises(
        ValueError,
        match="required dimension_id must not be empty",
    ):
        evaluate_context_scope(
            build_snapshot(),
            required_dimension_ids=(123,),
        )


def test_scope_rejects_duplicate_requirement_identity() -> None:
    with pytest.raises(
        ValueError,
        match="duplicate required dimension_id: CTX-FIXTURE-001",
    ):
        evaluate_context_scope(
            build_snapshot(),
            required_dimension_ids=(
                "CTX-FIXTURE-001",
                "CTX-FIXTURE-001",
            ),
        )


def test_scoped_evaluation_vocabulary_is_exact() -> None:
    assert {
        status.value
        for status in ScopedEvaluationStatus
    } == {
        "EVALUABLE",
        "INSUFFICIENT_EVIDENCE",
        "DISPUTED",
    }
