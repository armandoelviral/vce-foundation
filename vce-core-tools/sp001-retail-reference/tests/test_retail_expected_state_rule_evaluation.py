from dataclasses import (
    FrozenInstanceError,
    fields,
    replace,
)

import pytest

from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)
from sp001.contracts.retail_expected_state_rule_evaluation import (
    ExpectedStateRuleEvaluationResult,
    ExpectedStateRuleEvaluationStatus,
    evaluate_retail_expected_state_rule,
)
from test_retail_expected_state import (
    create_definition,
    create_snapshot,
)
from test_retail_expected_state_rule import (
    create_rule,
)


def create_dimension(
    *,
    dimension_id: str,
    dimension_type: str,
    value: str | None,
    applicability: DimensionApplicability = (
        DimensionApplicability.REQUIRED
    ),
    evidence_status: DimensionEvidenceStatus = (
        DimensionEvidenceStatus.DOCUMENTED
    ),
) -> RetailContextDimension:
    return RetailContextDimension(
        dimension_id=dimension_id,
        dimension_type=dimension_type,
        applicability=applicability,
        evidence_status=evidence_status,
        value=value,
    )


def create_evaluation(
    *,
    snapshot=None,
    rule=None,
) -> ExpectedStateRuleEvaluationResult:
    active_snapshot = (
        snapshot
        if snapshot is not None
        else create_snapshot()
    )

    active_rule = (
        rule
        if rule is not None
        else create_rule(
            context_definition=(
                active_snapshot.context_definition
            ),
        )
    )

    return evaluate_retail_expected_state_rule(
        rule=active_rule,
        snapshot=active_snapshot,
    )


def test_evaluation_declares_exact_result_contract() -> None:
    assert tuple(
        field.name
        for field in fields(
            ExpectedStateRuleEvaluationResult,
        )
    ) == (
        "expected_state_rule_id",
        "expected_state_rule_version",
        "snapshot_id",
        "snapshot_version",
        "context_definition_id",
        "definition_version",
        "status",
        "matched_dimension_ids",
        "missing_dimension_types",
        "insufficient_evidence_dimension_types",
        "disputed_dimension_types",
        "mismatched_dimension_types",
    )


def test_matching_conditions_are_applicable() -> None:
    result = create_evaluation()

    assert result.status is (
        ExpectedStateRuleEvaluationStatus.APPLICABLE
    )


def test_evaluation_preserves_rule_identity_and_version() -> None:
    snapshot = create_snapshot()

    rule = create_rule(
        expected_state_rule_id="EXPECTED-RULE-009",
        expected_state_rule_version=3,
        context_definition=(
            snapshot.context_definition
        ),
    )

    result = create_evaluation(
        snapshot=snapshot,
        rule=rule,
    )

    assert result.expected_state_rule_id == (
        "EXPECTED-RULE-009"
    )

    assert result.expected_state_rule_version == 3


def test_evaluation_preserves_snapshot_identity_and_version() -> None:
    snapshot = replace(
        create_snapshot(),
        snapshot_id="SNAPSHOT-STORE-A-V4",
        snapshot_version=4,
    )

    result = create_evaluation(
        snapshot=snapshot,
    )

    assert result.snapshot_id == (
        "SNAPSHOT-STORE-A-V4"
    )

    assert result.snapshot_version == 4


def test_evaluation_preserves_customer_definition_identity() -> None:
    result = create_evaluation()

    assert result.context_definition_id == (
        "DEFINITION-CUSTOMER-A"
    )

    assert result.definition_version == 1


def test_evaluation_preserves_matched_dimension_id_order() -> None:
    result = create_evaluation()

    assert result.matched_dimension_ids == (
        "DIM-DEPARTMENT-001",
        "DIM-INVENTORY-001",
    )


def test_evaluation_rejects_invalid_rule() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "rule must be a "
            "RetailExpectedStateRule"
        ),
    ):
        evaluate_retail_expected_state_rule(
            rule="EXPECTED-RULE-001",
            snapshot=create_snapshot(),
        )


def test_evaluation_rejects_invalid_snapshot() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "snapshot must be a "
            "RetailContextSnapshot"
        ),
    ):
        evaluate_retail_expected_state_rule(
            rule=create_rule(),
            snapshot="SNAPSHOT-STORE-A",
        )


def test_evaluation_rejects_snapshot_without_customer_definition() -> None:
    snapshot = create_snapshot(
        include_definition=False,
    )

    with pytest.raises(
        ValueError,
        match=(
            "snapshot requires "
            "context_definition"
        ),
    ):
        evaluate_retail_expected_state_rule(
            rule=create_rule(),
            snapshot=snapshot,
        )


def test_evaluation_rejects_snapshot_without_operating_scope() -> None:
    snapshot = create_snapshot(
        include_scope=False,
    )

    rule = create_rule(
        context_definition=(
            snapshot.context_definition
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "snapshot requires "
            "context_scope"
        ),
    ):
        evaluate_retail_expected_state_rule(
            rule=rule,
            snapshot=snapshot,
        )


def test_evaluation_rejects_rule_from_different_customer() -> None:
    snapshot = create_snapshot()

    foreign_definition = create_definition(
        context_definition_id=(
            "DEFINITION-CUSTOMER-B"
        ),
        customer_id="CUSTOMER-B",
    )

    foreign_rule = create_rule(
        context_definition=(
            foreign_definition
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "rule customer must match "
            "snapshot customer"
        ),
    ):
        evaluate_retail_expected_state_rule(
            rule=foreign_rule,
            snapshot=snapshot,
        )


def test_evaluation_rejects_different_customer_definition_identity() -> None:
    snapshot = create_snapshot()

    different_definition = create_definition(
        context_definition_id=(
            "DEFINITION-CUSTOMER-A-OTHER"
        ),
        customer_id="CUSTOMER-A",
    )

    rule = create_rule(
        context_definition=(
            different_definition
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "rule context_definition must match "
            "snapshot context_definition"
        ),
    ):
        evaluate_retail_expected_state_rule(
            rule=rule,
            snapshot=snapshot,
        )


def test_evaluation_rejects_different_customer_definition_version() -> None:
    snapshot = create_snapshot()

    different_definition = replace(
        snapshot.context_definition,
        definition_version=2,
    )

    rule = create_rule(
        context_definition=(
            different_definition
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "rule definition_version must match "
            "snapshot definition_version"
        ),
    ):
        evaluate_retail_expected_state_rule(
            rule=rule,
            snapshot=snapshot,
        )


def test_missing_dimension_is_reported_without_synthesis() -> None:
    snapshot = create_snapshot()

    snapshot = replace(
        snapshot,
        dimensions=(
            snapshot.dimensions[0],
        ),
    )

    result = create_evaluation(
        snapshot=snapshot,
    )

    assert result.status is (
        ExpectedStateRuleEvaluationStatus.INSUFFICIENT_EVIDENCE
    )

    assert result.missing_dimension_types == (
        "INVENTORY_STATE",
    )

    assert result.insufficient_evidence_dimension_types == ()

    assert len(
        snapshot.dimensions,
    ) == 1


def test_present_insufficient_evidence_is_distinct_from_absence() -> None:
    snapshot = create_snapshot()

    inventory = create_dimension(
        dimension_id="DIM-INVENTORY-001",
        dimension_type="INVENTORY_STATE",
        value=None,
        evidence_status=(
            DimensionEvidenceStatus.INSUFFICIENT_EVIDENCE
        ),
    )

    snapshot = replace(
        snapshot,
        dimensions=(
            snapshot.dimensions[0],
            inventory,
        ),
    )

    result = create_evaluation(
        snapshot=snapshot,
    )

    assert result.status is (
        ExpectedStateRuleEvaluationStatus.INSUFFICIENT_EVIDENCE
    )

    assert result.missing_dimension_types == ()

    assert result.insufficient_evidence_dimension_types == (
        "INVENTORY_STATE",
    )


def test_not_provided_evidence_is_distinct_from_absence() -> None:
    snapshot = create_snapshot()

    inventory = create_dimension(
        dimension_id="DIM-INVENTORY-001",
        dimension_type="INVENTORY_STATE",
        value=None,
        evidence_status=(
            DimensionEvidenceStatus.NOT_PROVIDED
        ),
    )

    snapshot = replace(
        snapshot,
        dimensions=(
            snapshot.dimensions[0],
            inventory,
        ),
    )

    result = create_evaluation(
        snapshot=snapshot,
    )

    assert result.status is (
        ExpectedStateRuleEvaluationStatus.INSUFFICIENT_EVIDENCE
    )

    assert result.missing_dimension_types == ()

    assert result.insufficient_evidence_dimension_types == (
        "INVENTORY_STATE",
    )


def test_disputed_evidence_is_reported_explicitly() -> None:
    snapshot = create_snapshot()

    disputed_department = create_dimension(
        dimension_id="DIM-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
        value="GIRLS",
        evidence_status=(
            DimensionEvidenceStatus.DISPUTED
        ),
    )

    snapshot = replace(
        snapshot,
        dimensions=(
            disputed_department,
            snapshot.dimensions[1],
        ),
    )

    result = create_evaluation(
        snapshot=snapshot,
    )

    assert result.status is (
        ExpectedStateRuleEvaluationStatus.DISPUTED
    )

    assert result.disputed_dimension_types == (
        "DEPARTMENT",
    )


def test_disputed_applicability_is_reported_explicitly() -> None:
    snapshot = create_snapshot()

    disputed_department = create_dimension(
        dimension_id="DIM-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
        value="GIRLS",
        applicability=(
            DimensionApplicability.DISPUTED
        ),
    )

    snapshot = replace(
        snapshot,
        dimensions=(
            disputed_department,
            snapshot.dimensions[1],
        ),
    )

    result = create_evaluation(
        snapshot=snapshot,
    )

    assert result.status is (
        ExpectedStateRuleEvaluationStatus.DISPUTED
    )

    assert result.disputed_dimension_types == (
        "DEPARTMENT",
    )


def test_disputed_evidence_takes_precedence_over_missing_dimension() -> None:
    snapshot = create_snapshot()

    disputed_department = create_dimension(
        dimension_id="DIM-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
        value="GIRLS",
        evidence_status=(
            DimensionEvidenceStatus.DISPUTED
        ),
    )

    snapshot = replace(
        snapshot,
        dimensions=(
            disputed_department,
        ),
    )

    result = create_evaluation(
        snapshot=snapshot,
    )

    assert result.status is (
        ExpectedStateRuleEvaluationStatus.DISPUTED
    )

    assert result.disputed_dimension_types == (
        "DEPARTMENT",
    )

    assert result.missing_dimension_types == (
        "INVENTORY_STATE",
    )


def test_incompatible_dimension_value_is_not_applicable() -> None:
    snapshot = create_snapshot()

    inventory = create_dimension(
        dimension_id="DIM-INVENTORY-001",
        dimension_type="INVENTORY_STATE",
        value="UNAVAILABLE",
    )

    snapshot = replace(
        snapshot,
        dimensions=(
            snapshot.dimensions[0],
            inventory,
        ),
    )

    result = create_evaluation(
        snapshot=snapshot,
    )

    assert result.status is (
        ExpectedStateRuleEvaluationStatus.NOT_APPLICABLE
    )

    assert result.mismatched_dimension_types == (
        "INVENTORY_STATE",
    )


def test_not_applicable_dimension_does_not_match_condition() -> None:
    snapshot = create_snapshot()

    inventory = create_dimension(
        dimension_id="DIM-INVENTORY-001",
        dimension_type="INVENTORY_STATE",
        value=None,
        applicability=(
            DimensionApplicability.NOT_APPLICABLE
        ),
        evidence_status=(
            DimensionEvidenceStatus.NOT_PROVIDED
        ),
    )

    snapshot = replace(
        snapshot,
        dimensions=(
            snapshot.dimensions[0],
            inventory,
        ),
    )

    result = create_evaluation(
        snapshot=snapshot,
    )

    assert result.status is (
        ExpectedStateRuleEvaluationStatus.NOT_APPLICABLE
    )

    assert result.mismatched_dimension_types == (
        "INVENTORY_STATE",
    )


def test_unrelated_disputed_dimension_does_not_block_rule() -> None:
    snapshot = create_snapshot()

    rule = create_rule(
        context_definition=(
            snapshot.context_definition
        ),
        required_dimension_values=(
            (
                "DEPARTMENT",
                "GIRLS",
            ),
        ),
    )

    disputed_inventory = create_dimension(
        dimension_id="DIM-INVENTORY-001",
        dimension_type="INVENTORY_STATE",
        value="AVAILABLE",
        evidence_status=(
            DimensionEvidenceStatus.DISPUTED
        ),
    )

    snapshot = replace(
        snapshot,
        dimensions=(
            snapshot.dimensions[0],
            disputed_inventory,
        ),
    )

    result = create_evaluation(
        snapshot=snapshot,
        rule=rule,
    )

    assert result.status is (
        ExpectedStateRuleEvaluationStatus.APPLICABLE
    )

    assert result.disputed_dimension_types == ()


def test_condition_order_controls_matched_dimension_order() -> None:
    snapshot = create_snapshot()

    rule = create_rule(
        context_definition=(
            snapshot.context_definition
        ),
        required_dimension_values=(
            (
                "INVENTORY_STATE",
                "AVAILABLE",
            ),
            (
                "DEPARTMENT",
                "GIRLS",
            ),
        ),
    )

    result = create_evaluation(
        snapshot=snapshot,
        rule=rule,
    )

    assert result.matched_dimension_ids == (
        "DIM-INVENTORY-001",
        "DIM-DEPARTMENT-001",
    )


def test_rule_evaluation_result_is_immutable() -> None:
    result = create_evaluation()

    with pytest.raises(
        FrozenInstanceError,
    ):
        result.snapshot_id = (
            "SNAPSHOT-OTHER"
        )


def test_evaluation_does_not_mutate_snapshot_or_rule() -> None:
    snapshot = create_snapshot()

    rule = create_rule(
        context_definition=(
            snapshot.context_definition
        ),
    )

    original_dimensions = snapshot.dimensions

    original_conditions = (
        rule.required_dimension_values
    )

    create_evaluation(
        snapshot=snapshot,
        rule=rule,
    )

    assert snapshot.dimensions == (
        original_dimensions
    )

    assert rule.required_dimension_values == (
        original_conditions
    )


def test_evaluation_does_not_generate_expected_state_or_recommendation() -> None:
    result = create_evaluation()

    for attribute in (
        "expected_state",
        "expected_value",
        "recommendation",
        "compliance_status",
        "authority",
        "commercial_impact",
        "customer_acceptance",
    ):
        assert not hasattr(
            result,
            attribute,
        )
