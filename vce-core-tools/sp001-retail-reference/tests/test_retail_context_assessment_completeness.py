from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.contracts.retail_context_definition import (
    RetailContextDefinition,
)
from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)
from sp001.contracts.retail_context_snapshot_completeness import (
    SnapshotCompletenessResult,
    SnapshotCompletenessStatus,
)
from sp001.services.retail_context_assessment import (
    RetailContextAssessmentResult,
    execute_retail_context_assessment,
)
from sp001.services.retail_context_assessment_report import (
    build_retail_context_assessment_report,
)

from test_rcp001_tcp_sears_canonical_matrix import (
    create_canonical_comparisons,
    create_canonical_graph,
    create_canonical_summary,
)


def create_definition(
    *,
    context_definition_id: str = "RCP-DEFINITION-001",
    customer_id: str = "CUSTOMER-001",
    definition_version: int = 3,
    dimension_types: tuple[str, ...] = (
        "DEPARTMENT",
        "INVENTORY_STATE",
        "PRESENTATION_CAPACITY",
    ),
    required_dimension_types: tuple[str, ...] = (
        "DEPARTMENT",
        "INVENTORY_STATE",
    ),
    optional_dimension_types: tuple[str, ...] = (
        "PRESENTATION_CAPACITY",
    ),
) -> RetailContextDefinition:
    return RetailContextDefinition(
        context_definition_id=context_definition_id,
        customer_id=customer_id,
        definition_version=definition_version,
        dimension_types=dimension_types,
        required_dimension_types=required_dimension_types,
        optional_dimension_types=optional_dimension_types,
    )


def create_dimension(
    *,
    dimension_id: str,
    dimension_type: str,
    applicability: DimensionApplicability = (
        DimensionApplicability.REQUIRED
    ),
    evidence_status: DimensionEvidenceStatus = (
        DimensionEvidenceStatus.DOCUMENTED
    ),
    value: str | None = "DECLARED_VALUE",
) -> RetailContextDimension:
    return RetailContextDimension(
        dimension_id=dimension_id,
        dimension_type=dimension_type,
        applicability=applicability,
        evidence_status=evidence_status,
        value=value,
    )


def create_snapshot(
    *,
    context_definition: RetailContextDefinition | None = None,
    dimensions: tuple[RetailContextDimension, ...] = (),
) -> RetailContextSnapshot:
    summary = create_canonical_summary()

    return RetailContextSnapshot(
        snapshot_id=summary.snapshot_id,
        snapshot_version=summary.snapshot_version,
        case_id=summary.case_id,
        context_definition=context_definition,
        dimensions=dimensions,
    )


def create_assessment(
    *,
    snapshot: RetailContextSnapshot,
) -> RetailContextAssessmentResult:
    graph = create_canonical_graph()

    return execute_retail_context_assessment(
        snapshot=snapshot,
        comparisons=create_canonical_comparisons(),
        provenance_records=graph.records,
        context_policy_ids=graph.context_policy_ids,
    )


def complete_required_dimensions() -> tuple[
    RetailContextDimension,
    ...,
]:
    return (
        create_dimension(
            dimension_id="DIM-DEPARTMENT",
            dimension_type="DEPARTMENT",
        ),
        create_dimension(
            dimension_id="DIM-INVENTORY",
            dimension_type="INVENTORY_STATE",
        ),
    )


def test_assessment_result_appends_optional_context_completeness() -> None:
    assert tuple(
        field.name
        for field in fields(
            RetailContextAssessmentResult,
        )
    ) == (
        "snapshot",
        "provenance_graph",
        "summary",
        "context_completeness",
    )


def test_assessment_service_materializes_completeness_result() -> None:
    result = create_assessment(
        snapshot=create_snapshot(),
    )

    assert isinstance(
        result.context_completeness,
        SnapshotCompletenessResult,
    )


def test_historical_result_construction_preserves_optional_completeness() -> None:
    current = create_assessment(
        snapshot=create_snapshot(),
    )

    historical = RetailContextAssessmentResult(
        snapshot=current.snapshot,
        provenance_graph=current.provenance_graph,
        summary=current.summary,
    )

    assert historical.context_completeness is None


def test_snapshot_without_definition_remains_not_established() -> None:
    result = create_assessment(
        snapshot=create_snapshot(),
    )

    assert result.context_completeness.status is (
        SnapshotCompletenessStatus.NOT_ESTABLISHED
    )


def test_historical_unclassified_definition_remains_not_established() -> None:
    definition = RetailContextDefinition(
        context_definition_id="RCP-DEFINITION-HISTORICAL",
        customer_id="CUSTOMER-001",
        definition_version=1,
        dimension_types=(
            "DEPARTMENT",
            "INVENTORY_STATE",
        ),
    )

    result = create_assessment(
        snapshot=create_snapshot(
            context_definition=definition,
        ),
    )

    assert result.context_completeness.status is (
        SnapshotCompletenessStatus.NOT_ESTABLISHED
    )


def test_documented_required_dimensions_are_complete() -> None:
    result = create_assessment(
        snapshot=create_snapshot(
            context_definition=create_definition(),
            dimensions=complete_required_dimensions(),
        ),
    )

    assert result.context_completeness.status is (
        SnapshotCompletenessStatus.COMPLETE
    )


def test_missing_required_dimensions_remain_incomplete() -> None:
    result = create_assessment(
        snapshot=create_snapshot(
            context_definition=create_definition(),
            dimensions=(),
        ),
    )

    assert result.context_completeness.status is (
        SnapshotCompletenessStatus.INCOMPLETE
    )
    assert result.context_completeness.missing_required_dimension_types == (
        "DEPARTMENT",
        "INVENTORY_STATE",
    )


def test_missing_required_dimension_order_is_preserved() -> None:
    result = create_assessment(
        snapshot=create_snapshot(
            context_definition=create_definition(),
            dimensions=(
                create_dimension(
                    dimension_id="DIM-DEPARTMENT",
                    dimension_type="DEPARTMENT",
                ),
            ),
        ),
    )

    assert result.context_completeness.missing_required_dimension_types == (
        "INVENTORY_STATE",
    )


def test_insufficient_required_evidence_remains_indeterminate() -> None:
    result = create_assessment(
        snapshot=create_snapshot(
            context_definition=create_definition(),
            dimensions=(
                create_dimension(
                    dimension_id="DIM-DEPARTMENT",
                    dimension_type="DEPARTMENT",
                ),
                create_dimension(
                    dimension_id="DIM-INVENTORY",
                    dimension_type="INVENTORY_STATE",
                    evidence_status=(
                        DimensionEvidenceStatus.NOT_PROVIDED
                    ),
                    value=None,
                ),
            ),
        ),
    )

    assert result.context_completeness.status is (
        SnapshotCompletenessStatus.INDETERMINATE
    )
    assert result.context_completeness.insufficient_evidence_dimension_types == (
        "INVENTORY_STATE",
    )


def test_disputed_required_evidence_remains_indeterminate() -> None:
    result = create_assessment(
        snapshot=create_snapshot(
            context_definition=create_definition(),
            dimensions=(
                create_dimension(
                    dimension_id="DIM-DEPARTMENT",
                    dimension_type="DEPARTMENT",
                ),
                create_dimension(
                    dimension_id="DIM-INVENTORY",
                    dimension_type="INVENTORY_STATE",
                    evidence_status=(
                        DimensionEvidenceStatus.DISPUTED
                    ),
                    value=None,
                ),
            ),
        ),
    )

    assert result.context_completeness.status is (
        SnapshotCompletenessStatus.INDETERMINATE
    )
    assert result.context_completeness.disputed_dimension_types == (
        "INVENTORY_STATE",
    )


def test_disputed_evidence_takes_priority_over_missing_dimensions() -> None:
    result = create_assessment(
        snapshot=create_snapshot(
            context_definition=create_definition(),
            dimensions=(
                create_dimension(
                    dimension_id="DIM-DEPARTMENT",
                    dimension_type="DEPARTMENT",
                    evidence_status=(
                        DimensionEvidenceStatus.DISPUTED
                    ),
                    value=None,
                ),
            ),
        ),
    )

    assert result.context_completeness.status is (
        SnapshotCompletenessStatus.INDETERMINATE
    )
    assert result.context_completeness.disputed_dimension_types == (
        "DEPARTMENT",
    )
    assert result.context_completeness.missing_required_dimension_types == (
        "INVENTORY_STATE",
    )


def test_missing_optional_dimension_does_not_block_assessment() -> None:
    result = create_assessment(
        snapshot=create_snapshot(
            context_definition=create_definition(),
            dimensions=complete_required_dimensions(),
        ),
    )

    assert result.context_completeness.status is (
        SnapshotCompletenessStatus.COMPLETE
    )
    assert "PRESENTATION_CAPACITY" not in (
        result.context_completeness.missing_required_dimension_types
    )


def test_disputed_optional_dimension_does_not_block_required_completeness() -> None:
    result = create_assessment(
        snapshot=create_snapshot(
            context_definition=create_definition(),
            dimensions=(
                *complete_required_dimensions(),
                create_dimension(
                    dimension_id="DIM-CAPACITY",
                    dimension_type="PRESENTATION_CAPACITY",
                    applicability=(
                        DimensionApplicability.DISPUTED
                    ),
                    evidence_status=(
                        DimensionEvidenceStatus.DISPUTED
                    ),
                    value=None,
                ),
            ),
        ),
    )

    assert result.context_completeness.status is (
        SnapshotCompletenessStatus.COMPLETE
    )
    assert result.context_completeness.disputed_dimension_types == ()


def test_completeness_preserves_assessment_snapshot_identity() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
    )

    result = create_assessment(
        snapshot=snapshot,
    )

    assert result.context_completeness.snapshot_id == (
        snapshot.snapshot_id
    )
    assert result.context_completeness.snapshot_version == (
        snapshot.snapshot_version
    )
    assert result.context_completeness.case_id == (
        snapshot.case_id
    )


def test_completeness_preserves_customer_definition_identity() -> None:
    definition = create_definition(
        context_definition_id="RCP-DEFINITION-VERSIONED",
        definition_version=9,
    )

    result = create_assessment(
        snapshot=create_snapshot(
            context_definition=definition,
        ),
    )

    assert result.context_completeness.context_definition_id == (
        "RCP-DEFINITION-VERSIONED"
    )
    assert result.context_completeness.definition_version == 9


def test_completeness_does_not_change_provenance_or_improvement_accounting() -> None:
    result = create_assessment(
        snapshot=create_snapshot(
            context_definition=create_definition(),
            dimensions=(),
        ),
    )

    assert result.provenance_graph.total_rules == 35
    assert result.summary.total_improved_count == 14
    assert result.context_completeness.status is (
        SnapshotCompletenessStatus.INCOMPLETE
    )


def test_existing_assessment_report_remains_compatible() -> None:
    result = create_assessment(
        snapshot=create_snapshot(
            context_definition=create_definition(),
            dimensions=(),
        ),
    )

    report = build_retail_context_assessment_report(
        result=result,
    )

    assert report.total_rules == 35
    assert report.customer_acceptance_status == (
        "NOT_ESTABLISHED"
    )
    assert report.commercial_impact_status == (
        "NOT_ESTABLISHED"
    )


def test_assessment_does_not_mutate_snapshot_or_synthesize_dimensions() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
        dimensions=(),
    )

    original_dimensions = snapshot.dimensions

    result = create_assessment(
        snapshot=snapshot,
    )

    assert snapshot.dimensions is original_dimensions
    assert snapshot.dimensions == ()
    assert result.context_completeness.missing_required_dimension_types == (
        "DEPARTMENT",
        "INVENTORY_STATE",
    )


def test_assessment_result_with_completeness_remains_immutable() -> None:
    result = create_assessment(
        snapshot=create_snapshot(),
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        result.context_completeness = None


def test_completeness_does_not_infer_compliance_authority_or_outcomes() -> None:
    result = create_assessment(
        snapshot=create_snapshot(
            context_definition=create_definition(),
        ),
    )

    for attribute in (
        "compliance_status",
        "commercial_impact_status",
        "customer_acceptance_status",
        "authority",
        "owner",
        "inferred_values",
    ):
        assert not hasattr(
            result.context_completeness,
            attribute,
        )
