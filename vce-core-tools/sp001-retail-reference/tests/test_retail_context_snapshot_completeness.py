from dataclasses import FrozenInstanceError

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
    evaluate_retail_context_snapshot_completeness,
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
    snapshot_id: str = "RCP-SNAPSHOT-001",
    snapshot_version: int = 7,
    case_id: str = "CASE-001",
    context_definition: RetailContextDefinition | None = None,
    dimensions: tuple[RetailContextDimension, ...] = (),
) -> RetailContextSnapshot:
    return RetailContextSnapshot(
        snapshot_id=snapshot_id,
        snapshot_version=snapshot_version,
        case_id=case_id,
        context_definition=context_definition,
        dimensions=dimensions,
    )


def test_completeness_vocabulary_is_exact() -> None:
    assert {
        status.value
        for status in SnapshotCompletenessStatus
    } == {
        "NOT_ESTABLISHED",
        "COMPLETE",
        "INCOMPLETE",
        "INDETERMINATE",
    }


def test_evaluator_rejects_non_snapshot_input() -> None:
    with pytest.raises(
        TypeError,
        match="snapshot must be a RetailContextSnapshot",
    ):
        evaluate_retail_context_snapshot_completeness(
            snapshot=None,
        )


def test_snapshot_without_definition_is_not_established() -> None:
    snapshot = create_snapshot()

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert result.status is (
        SnapshotCompletenessStatus.NOT_ESTABLISHED
    )
    assert result.context_definition_id is None
    assert result.definition_version is None
    assert result.required_dimension_types == ()
    assert result.missing_required_dimension_types == ()


def test_historical_unclassified_definition_is_not_established() -> None:
    definition = RetailContextDefinition(
        context_definition_id="RCP-DEFINITION-HISTORICAL",
        customer_id="CUSTOMER-001",
        definition_version=1,
        dimension_types=(
            "DEPARTMENT",
            "INVENTORY_STATE",
        ),
    )

    snapshot = create_snapshot(
        context_definition=definition,
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert result.status is (
        SnapshotCompletenessStatus.NOT_ESTABLISHED
    )
    assert result.context_definition_id == (
        "RCP-DEFINITION-HISTORICAL"
    )
    assert result.definition_version == 1


def test_result_preserves_snapshot_identity() -> None:
    snapshot = create_snapshot(
        snapshot_id="RCP-SNAPSHOT-IDENTITY",
        snapshot_version=11,
        case_id="CASE-IDENTITY",
        context_definition=create_definition(),
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert result.snapshot_id == "RCP-SNAPSHOT-IDENTITY"
    assert result.snapshot_version == 11
    assert result.case_id == "CASE-IDENTITY"


def test_result_preserves_customer_definition_identity_and_version() -> None:
    definition = create_definition(
        context_definition_id="RCP-DEFINITION-VERSIONED",
        definition_version=9,
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=create_snapshot(
            context_definition=definition,
        ),
    )

    assert result.context_definition_id == (
        "RCP-DEFINITION-VERSIONED"
    )
    assert result.definition_version == 9
    assert result.required_dimension_types == (
        "DEPARTMENT",
        "INVENTORY_STATE",
    )


def test_explicit_configuration_with_only_optional_dimensions_is_complete() -> None:
    definition = create_definition(
        dimension_types=(
            "PRESENTATION_CAPACITY",
        ),
        required_dimension_types=(),
        optional_dimension_types=(
            "PRESENTATION_CAPACITY",
        ),
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=create_snapshot(
            context_definition=definition,
        ),
    )

    assert result.status is (
        SnapshotCompletenessStatus.COMPLETE
    )
    assert result.required_dimension_types == ()


def test_all_documented_required_dimensions_are_complete() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
        dimensions=(
            create_dimension(
                dimension_id="DIM-DEPARTMENT",
                dimension_type="DEPARTMENT",
            ),
            create_dimension(
                dimension_id="DIM-INVENTORY",
                dimension_type="INVENTORY_STATE",
            ),
        ),
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert isinstance(
        result,
        SnapshotCompletenessResult,
    )
    assert result.status is (
        SnapshotCompletenessStatus.COMPLETE
    )
    assert result.missing_required_dimension_types == ()
    assert result.insufficient_evidence_dimension_types == ()
    assert result.disputed_dimension_types == ()


@pytest.mark.parametrize(
    "evidence_status",
    (
        DimensionEvidenceStatus.DOCUMENTED,
        DimensionEvidenceStatus.HUMAN_DECLARED,
        DimensionEvidenceStatus.MEASURED,
        DimensionEvidenceStatus.INDEPENDENTLY_VERIFIED,
    ),
)
def test_supported_evidence_statuses_can_establish_completeness(
    evidence_status: DimensionEvidenceStatus,
) -> None:
    definition = create_definition(
        dimension_types=(
            "DEPARTMENT",
        ),
        required_dimension_types=(
            "DEPARTMENT",
        ),
        optional_dimension_types=(),
    )

    snapshot = create_snapshot(
        context_definition=definition,
        dimensions=(
            create_dimension(
                dimension_id="DIM-DEPARTMENT",
                dimension_type="DEPARTMENT",
                evidence_status=evidence_status,
            ),
        ),
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert result.status is (
        SnapshotCompletenessStatus.COMPLETE
    )


def test_missing_required_dimension_is_incomplete() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
        dimensions=(
            create_dimension(
                dimension_id="DIM-DEPARTMENT",
                dimension_type="DEPARTMENT",
            ),
        ),
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert result.status is (
        SnapshotCompletenessStatus.INCOMPLETE
    )
    assert result.missing_required_dimension_types == (
        "INVENTORY_STATE",
    )


def test_missing_required_dimension_order_follows_customer_definition() -> None:
    result = evaluate_retail_context_snapshot_completeness(
        snapshot=create_snapshot(
            context_definition=create_definition(),
        ),
    )

    assert result.status is (
        SnapshotCompletenessStatus.INCOMPLETE
    )
    assert result.missing_required_dimension_types == (
        "DEPARTMENT",
        "INVENTORY_STATE",
    )


def test_missing_optional_dimension_does_not_block_completeness() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
        dimensions=(
            create_dimension(
                dimension_id="DIM-DEPARTMENT",
                dimension_type="DEPARTMENT",
            ),
            create_dimension(
                dimension_id="DIM-INVENTORY",
                dimension_type="INVENTORY_STATE",
            ),
        ),
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert result.status is (
        SnapshotCompletenessStatus.COMPLETE
    )
    assert "PRESENTATION_CAPACITY" not in (
        result.missing_required_dimension_types
    )


def test_disputed_optional_dimension_does_not_block_required_completeness() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
        dimensions=(
            create_dimension(
                dimension_id="DIM-DEPARTMENT",
                dimension_type="DEPARTMENT",
            ),
            create_dimension(
                dimension_id="DIM-INVENTORY",
                dimension_type="INVENTORY_STATE",
            ),
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
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert result.status is (
        SnapshotCompletenessStatus.COMPLETE
    )
    assert result.disputed_dimension_types == ()


def test_required_dimension_without_provided_evidence_is_indeterminate() -> None:
    snapshot = create_snapshot(
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
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert result.status is (
        SnapshotCompletenessStatus.INDETERMINATE
    )
    assert result.missing_required_dimension_types == ()
    assert result.insufficient_evidence_dimension_types == (
        "INVENTORY_STATE",
    )


def test_required_dimension_with_insufficient_evidence_is_indeterminate() -> None:
    snapshot = create_snapshot(
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
                    DimensionEvidenceStatus.INSUFFICIENT_EVIDENCE
                ),
                value=None,
            ),
        ),
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert result.status is (
        SnapshotCompletenessStatus.INDETERMINATE
    )
    assert result.insufficient_evidence_dimension_types == (
        "INVENTORY_STATE",
    )


def test_required_dimension_with_disputed_evidence_is_indeterminate() -> None:
    snapshot = create_snapshot(
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
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert result.status is (
        SnapshotCompletenessStatus.INDETERMINATE
    )
    assert result.disputed_dimension_types == (
        "INVENTORY_STATE",
    )


def test_required_dimension_with_disputed_applicability_is_indeterminate() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
        dimensions=(
            create_dimension(
                dimension_id="DIM-DEPARTMENT",
                dimension_type="DEPARTMENT",
            ),
            create_dimension(
                dimension_id="DIM-INVENTORY",
                dimension_type="INVENTORY_STATE",
                applicability=(
                    DimensionApplicability.DISPUTED
                ),
                evidence_status=(
                    DimensionEvidenceStatus.DOCUMENTED
                ),
                value="DECLARED_VALUE",
            ),
        ),
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert result.status is (
        SnapshotCompletenessStatus.INDETERMINATE
    )
    assert result.disputed_dimension_types == (
        "INVENTORY_STATE",
    )


def test_required_not_applicable_dimension_cannot_establish_completeness() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
        dimensions=(
            create_dimension(
                dimension_id="DIM-DEPARTMENT",
                dimension_type="DEPARTMENT",
            ),
            create_dimension(
                dimension_id="DIM-INVENTORY",
                dimension_type="INVENTORY_STATE",
                applicability=(
                    DimensionApplicability.NOT_APPLICABLE
                ),
                evidence_status=(
                    DimensionEvidenceStatus.NOT_PROVIDED
                ),
                value=None,
            ),
        ),
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert result.status is (
        SnapshotCompletenessStatus.INDETERMINATE
    )
    assert result.insufficient_evidence_dimension_types == (
        "INVENTORY_STATE",
    )


def test_disputed_required_dimension_takes_priority_over_missing_dimension() -> None:
    snapshot = create_snapshot(
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
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert result.status is (
        SnapshotCompletenessStatus.INDETERMINATE
    )
    assert result.disputed_dimension_types == (
        "DEPARTMENT",
    )
    assert result.missing_required_dimension_types == (
        "INVENTORY_STATE",
    )


def test_missing_dimension_and_insufficient_evidence_remain_distinguishable() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
        dimensions=(
            create_dimension(
                dimension_id="DIM-DEPARTMENT",
                dimension_type="DEPARTMENT",
                evidence_status=(
                    DimensionEvidenceStatus.INSUFFICIENT_EVIDENCE
                ),
                value=None,
            ),
        ),
    )

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert result.status is (
        SnapshotCompletenessStatus.INCOMPLETE
    )
    assert result.missing_required_dimension_types == (
        "INVENTORY_STATE",
    )
    assert result.insufficient_evidence_dimension_types == (
        "DEPARTMENT",
    )


def test_result_is_immutable() -> None:
    result = evaluate_retail_context_snapshot_completeness(
        snapshot=create_snapshot(
            context_definition=create_definition(),
        ),
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        result.status = (
            SnapshotCompletenessStatus.COMPLETE
        )


def test_evaluation_does_not_mutate_snapshot_or_synthesize_dimensions() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
        dimensions=(),
    )

    original_dimensions = snapshot.dimensions

    result = evaluate_retail_context_snapshot_completeness(
        snapshot=snapshot,
    )

    assert snapshot.dimensions is original_dimensions
    assert snapshot.dimensions == ()
    assert result.missing_required_dimension_types == (
        "DEPARTMENT",
        "INVENTORY_STATE",
    )


def test_evaluation_does_not_infer_compliance_authority_or_commercial_outcome() -> None:
    result = evaluate_retail_context_snapshot_completeness(
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
            result,
            attribute,
        )
