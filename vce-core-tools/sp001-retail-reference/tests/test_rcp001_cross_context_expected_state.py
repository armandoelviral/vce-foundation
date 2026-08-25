from dataclasses import replace

import pytest

from sp001.contracts.retail_context_dimension import (
    DimensionEvidenceStatus,
)
from sp001.contracts.retail_expected_state import (
    RetailExpectedState,
)
from sp001.contracts.retail_expected_state_rule_evaluation import (
    ExpectedStateRuleEvaluationStatus,
    evaluate_retail_expected_state_rule,
)
from sp001.services.retail_expected_state_generation import (
    generate_retail_expected_state,
)
from test_retail_expected_state import (
    create_definition,
    create_scope,
    create_snapshot,
)
from test_retail_expected_state_rule import (
    create_rule,
)
from test_retail_expected_state_rule_evaluation import (
    create_dimension,
)


def create_store_a_snapshot():
    definition = create_definition(
        context_definition_id=(
            "DEFINITION-CUSTOMER-A"
        ),
        customer_id="CUSTOMER-A",
    )

    scope = create_scope(
        context_id="CONTEXT-STORE-A",
        point_of_sale_id="STORE-A",
    )

    return create_snapshot(
        snapshot_id="SNAPSHOT-STORE-A",
        case_id="CASE-STORE-A",
        context_scope=scope,
        context_definition=definition,
    )


def create_store_b_snapshot():
    definition = create_definition(
        context_definition_id=(
            "DEFINITION-CUSTOMER-B"
        ),
        customer_id="CUSTOMER-B",
    )

    scope = create_scope(
        context_id="CONTEXT-STORE-B",
        point_of_sale_id="STORE-B",
    )

    return create_snapshot(
        snapshot_id="SNAPSHOT-STORE-B",
        case_id="CASE-STORE-B",
        context_scope=scope,
        context_definition=definition,
    )


def create_store_a_rule(
    snapshot,
):
    return create_rule(
        expected_state_rule_id=(
            "EXPECTED-RULE-CUSTOMER-A"
        ),
        context_definition=(
            snapshot.context_definition
        ),
        expectation_type=(
            "VISIBILITY_PRIORITY"
        ),
        expected_value="HERO",
        required_dimension_values=(
            (
                "DEPARTMENT",
                "GIRLS",
            ),
            (
                "INVENTORY_STATE",
                "AVAILABLE",
            ),
        ),
        source_policy_ids=(
            "POLICY-CUSTOMER-A-VISIBILITY",
        ),
    )


def create_store_b_rule(
    snapshot,
):
    return create_rule(
        expected_state_rule_id=(
            "EXPECTED-RULE-CUSTOMER-B"
        ),
        context_definition=(
            snapshot.context_definition
        ),
        expectation_type=(
            "VISIBILITY_PRIORITY"
        ),
        expected_value="SUPPORT",
        required_dimension_values=(
            (
                "DEPARTMENT",
                "GIRLS",
            ),
            (
                "INVENTORY_STATE",
                "AVAILABLE",
            ),
        ),
        source_policy_ids=(
            "POLICY-CUSTOMER-B-VISIBILITY",
        ),
    )


def create_cross_context_states():
    snapshot_a = create_store_a_snapshot()

    snapshot_b = create_store_b_snapshot()

    rule_a = create_store_a_rule(
        snapshot_a,
    )

    rule_b = create_store_b_rule(
        snapshot_b,
    )

    state_a = generate_retail_expected_state(
        expected_state_id=(
            "EXPECTED-STATE-STORE-A"
        ),
        expected_state_version=1,
        rule=rule_a,
        snapshot=snapshot_a,
    )

    state_b = generate_retail_expected_state(
        expected_state_id=(
            "EXPECTED-STATE-STORE-B"
        ),
        expected_state_version=1,
        rule=rule_b,
        snapshot=snapshot_b,
    )

    return (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    )


def test_stores_preserve_distinct_operating_contexts() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    assert (
        snapshot_a.context_scope.context_id
        == "CONTEXT-STORE-A"
    )

    assert (
        snapshot_b.context_scope.context_id
        == "CONTEXT-STORE-B"
    )

    assert (
        snapshot_a.context_scope.point_of_sale_id
        == "STORE-A"
    )

    assert (
        snapshot_b.context_scope.point_of_sale_id
        == "STORE-B"
    )


def test_stores_preserve_distinct_customer_definitions() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    assert (
        snapshot_a.context_definition.customer_id
        == "CUSTOMER-A"
    )

    assert (
        snapshot_b.context_definition.customer_id
        == "CUSTOMER-B"
    )

    assert (
        snapshot_a.context_definition.context_definition_id
        != snapshot_b.context_definition.context_definition_id
    )


def test_stores_preserve_distinct_case_and_snapshot_identities() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    assert snapshot_a.case_id == (
        "CASE-STORE-A"
    )

    assert snapshot_b.case_id == (
        "CASE-STORE-B"
    )

    assert snapshot_a.snapshot_id == (
        "SNAPSHOT-STORE-A"
    )

    assert snapshot_b.snapshot_id == (
        "SNAPSHOT-STORE-B"
    )


def test_stores_share_identical_context_dimension_values() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    values_a = tuple(
        (
            dimension.dimension_type,
            dimension.value,
        )
        for dimension in (
            snapshot_a.dimensions
        )
    )

    values_b = tuple(
        (
            dimension.dimension_type,
            dimension.value,
        )
        for dimension in (
            snapshot_b.dimensions
        )
    )

    assert values_a == values_b

    assert values_a == (
        (
            "DEPARTMENT",
            "GIRLS",
        ),
        (
            "INVENTORY_STATE",
            "AVAILABLE",
        ),
    )


def test_stores_share_identical_evidence_dimension_identities() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    dimension_ids_a = tuple(
        dimension.dimension_id
        for dimension in (
            snapshot_a.dimensions
        )
    )

    dimension_ids_b = tuple(
        dimension.dimension_id
        for dimension in (
            snapshot_b.dimensions
        )
    )

    assert dimension_ids_a == (
        dimension_ids_b
    )

    assert dimension_ids_a == (
        "DIM-DEPARTMENT-001",
        "DIM-INVENTORY-001",
    )


def test_customers_declare_identical_rule_conditions() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    assert (
        rule_a.required_dimension_values
        == rule_b.required_dimension_values
    )


def test_customer_rules_preserve_distinct_rule_identities() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    assert rule_a.expected_state_rule_id == (
        "EXPECTED-RULE-CUSTOMER-A"
    )

    assert rule_b.expected_state_rule_id == (
        "EXPECTED-RULE-CUSTOMER-B"
    )


def test_customer_rules_are_independently_applicable() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    evaluation_a = (
        evaluate_retail_expected_state_rule(
            rule=rule_a,
            snapshot=snapshot_a,
        )
    )

    evaluation_b = (
        evaluate_retail_expected_state_rule(
            rule=rule_b,
            snapshot=snapshot_b,
        )
    )

    assert evaluation_a.status is (
        ExpectedStateRuleEvaluationStatus.APPLICABLE
    )

    assert evaluation_b.status is (
        ExpectedStateRuleEvaluationStatus.APPLICABLE
    )


def test_customer_rules_preserve_same_expectation_type() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    assert rule_a.expectation_type == (
        "VISIBILITY_PRIORITY"
    )

    assert rule_b.expectation_type == (
        "VISIBILITY_PRIORITY"
    )


def test_customer_rules_declare_different_expected_values() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    assert rule_a.expected_value == (
        "HERO"
    )

    assert rule_b.expected_value == (
        "SUPPORT"
    )


def test_generated_states_reuse_existing_expected_state_contract() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    assert isinstance(
        state_a,
        RetailExpectedState,
    )

    assert isinstance(
        state_b,
        RetailExpectedState,
    )


def test_generated_states_preserve_distinct_identities() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    assert state_a.expected_state_id == (
        "EXPECTED-STATE-STORE-A"
    )

    assert state_b.expected_state_id == (
        "EXPECTED-STATE-STORE-B"
    )


def test_generated_states_preserve_distinct_customer_expectations() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    assert state_a.expectation_type == (
        state_b.expectation_type
    )

    assert state_a.expected_value == (
        "HERO"
    )

    assert state_b.expected_value == (
        "SUPPORT"
    )

    assert (
        state_a.expected_value
        != state_b.expected_value
    )


def test_generated_states_preserve_actual_matching_evidence() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    assert state_a.source_dimension_ids == (
        "DIM-DEPARTMENT-001",
        "DIM-INVENTORY-001",
    )

    assert (
        state_a.source_dimension_ids
        == state_b.source_dimension_ids
    )


def test_generated_states_preserve_customer_specific_policy_references() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    assert state_a.source_policy_ids == (
        "POLICY-CUSTOMER-A-VISIBILITY",
    )

    assert state_b.source_policy_ids == (
        "POLICY-CUSTOMER-B-VISIBILITY",
    )


def test_customer_a_rule_cannot_generate_state_for_customer_b() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    with pytest.raises(
        ValueError,
        match=(
            "rule customer must match "
            "snapshot customer"
        ),
    ):
        generate_retail_expected_state(
            expected_state_id=(
                "EXPECTED-CROSS-CUSTOMER"
            ),
            expected_state_version=1,
            rule=rule_a,
            snapshot=snapshot_b,
        )


def test_missing_store_evidence_prevents_expected_state_generation() -> None:
    snapshot = create_store_a_snapshot()

    incomplete_snapshot = replace(
        snapshot,
        dimensions=(
            snapshot.dimensions[0],
        ),
    )

    rule = create_store_a_rule(
        incomplete_snapshot,
    )

    with pytest.raises(
        ValueError,
        match=(
            "expected state requires "
            "an applicable rule: "
            "INSUFFICIENT_EVIDENCE"
        ),
    ):
        generate_retail_expected_state(
            expected_state_id=(
                "EXPECTED-STORE-A-INCOMPLETE"
            ),
            expected_state_version=1,
            rule=rule,
            snapshot=(
                incomplete_snapshot
            ),
        )

    assert len(
        incomplete_snapshot.dimensions,
    ) == 1


def test_disputed_store_evidence_prevents_expected_state_generation() -> None:
    snapshot = create_store_b_snapshot()

    disputed_department = create_dimension(
        dimension_id="DIM-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
        value="GIRLS",
        evidence_status=(
            DimensionEvidenceStatus.DISPUTED
        ),
    )

    disputed_snapshot = replace(
        snapshot,
        dimensions=(
            disputed_department,
            snapshot.dimensions[1],
        ),
    )

    rule = create_store_b_rule(
        disputed_snapshot,
    )

    with pytest.raises(
        ValueError,
        match=(
            "expected state requires "
            "an applicable rule: "
            "DISPUTED"
        ),
    ):
        generate_retail_expected_state(
            expected_state_id=(
                "EXPECTED-STORE-B-DISPUTED"
            ),
            expected_state_version=1,
            rule=rule,
            snapshot=(
                disputed_snapshot
            ),
        )


def test_incompatible_store_evidence_prevents_expected_state_generation() -> None:
    snapshot = create_store_b_snapshot()

    unavailable_inventory = create_dimension(
        dimension_id="DIM-INVENTORY-001",
        dimension_type="INVENTORY_STATE",
        value="UNAVAILABLE",
    )

    incompatible_snapshot = replace(
        snapshot,
        dimensions=(
            snapshot.dimensions[0],
            unavailable_inventory,
        ),
    )

    rule = create_store_b_rule(
        incompatible_snapshot,
    )

    with pytest.raises(
        ValueError,
        match=(
            "expected state requires "
            "an applicable rule: "
            "NOT_APPLICABLE"
        ),
    ):
        generate_retail_expected_state(
            expected_state_id=(
                "EXPECTED-STORE-B-INCOMPATIBLE"
            ),
            expected_state_version=1,
            rule=rule,
            snapshot=(
                incompatible_snapshot
            ),
        )


def test_generated_expectations_do_not_infer_compliance_or_authority() -> None:
    (
        snapshot_a,
        snapshot_b,
        rule_a,
        rule_b,
        state_a,
        state_b,
    ) = create_cross_context_states()

    for state in (
        state_a,
        state_b,
    ):
        for attribute in (
            "recommendation",
            "compliance_status",
            "commercial_impact",
            "customer_acceptance",
            "authority",
            "owner",
            "fixture_id",
            "sku_id",
            "facing_count",
        ):
            assert not hasattr(
                state,
                attribute,
            )
