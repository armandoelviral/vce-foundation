from dataclasses import (
    FrozenInstanceError,
    replace,
)

import pytest

from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
)
from sp001.contracts.retail_expected_state import (
    RetailExpectedState,
)
from sp001.services.retail_expected_state_generation import (
    generate_retail_expected_state,
)
from test_retail_expected_state import (
    create_definition,
    create_snapshot,
)
from test_retail_expected_state_rule import (
    create_rule,
)
from test_retail_expected_state_rule_evaluation import (
    create_dimension,
)


def generate_state(
    *,
    expected_state_id: str = "GENERATED-EXPECTED-001",
    expected_state_version: int = 1,
    snapshot=None,
    rule=None,
) -> RetailExpectedState:
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

    return generate_retail_expected_state(
        expected_state_id=(
            expected_state_id
        ),
        expected_state_version=(
            expected_state_version
        ),
        rule=active_rule,
        snapshot=active_snapshot,
    )


def test_generation_returns_existing_expected_state_contract() -> None:
    state = generate_state()

    assert isinstance(
        state,
        RetailExpectedState,
    )


def test_generation_preserves_explicit_expected_state_identity() -> None:
    state = generate_state(
        expected_state_id=(
            "GENERATED-EXPECTED-009"
        ),
    )

    assert state.expected_state_id == (
        "GENERATED-EXPECTED-009"
    )


@pytest.mark.parametrize(
    "invalid_identity",
    (
        "",
        "   ",
        None,
        123,
    ),
)
def test_generation_rejects_invalid_expected_state_identity(
    invalid_identity: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "expected_state_id "
            "must not be empty"
        ),
    ):
        generate_state(
            expected_state_id=(
                invalid_identity
            ),
        )


def test_generation_preserves_explicit_expected_state_version() -> None:
    state = generate_state(
        expected_state_version=4,
    )

    assert state.expected_state_version == 4


@pytest.mark.parametrize(
    "invalid_version",
    (
        0,
        -1,
        True,
        False,
        "1",
        None,
    ),
)
def test_generation_rejects_invalid_expected_state_version(
    invalid_version: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "expected_state_version "
            "must be a positive integer"
        ),
    ):
        generate_state(
            expected_state_version=(
                invalid_version
            ),
        )


def test_generation_preserves_exact_source_snapshot() -> None:
    snapshot = create_snapshot()

    state = generate_state(
        snapshot=snapshot,
    )

    assert state.snapshot is snapshot


def test_generation_preserves_customer_declared_expectation_type() -> None:
    snapshot = create_snapshot()

    rule = create_rule(
        context_definition=(
            snapshot.context_definition
        ),
        expectation_type=(
            "CUSTOMER_DEFINED_VISIBILITY"
        ),
    )

    state = generate_state(
        snapshot=snapshot,
        rule=rule,
    )

    assert state.expectation_type == (
        "CUSTOMER_DEFINED_VISIBILITY"
    )


def test_generation_preserves_customer_declared_expected_value() -> None:
    snapshot = create_snapshot()

    rule = create_rule(
        context_definition=(
            snapshot.context_definition
        ),
        expected_value="SUPPORT",
    )

    state = generate_state(
        snapshot=snapshot,
        rule=rule,
    )

    assert state.expected_value == (
        "SUPPORT"
    )


def test_generation_uses_only_matched_snapshot_dimension_ids() -> None:
    state = generate_state()

    assert state.source_dimension_ids == (
        "DIM-DEPARTMENT-001",
        "DIM-INVENTORY-001",
    )


def test_generation_preserves_customer_condition_order() -> None:
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

    state = generate_state(
        snapshot=snapshot,
        rule=rule,
    )

    assert state.source_dimension_ids == (
        "DIM-INVENTORY-001",
        "DIM-DEPARTMENT-001",
    )


def test_generation_excludes_unrelated_snapshot_dimensions() -> None:
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

    state = generate_state(
        snapshot=snapshot,
        rule=rule,
    )

    assert state.source_dimension_ids == (
        "DIM-DEPARTMENT-001",
    )


def test_generation_preserves_declared_policy_references() -> None:
    snapshot = create_snapshot()

    rule = create_rule(
        context_definition=(
            snapshot.context_definition
        ),
        source_policy_ids=(
            "CP01-CONTEXTUAL-ADAPTATION",
            "CP02-BRAND-VISIBILITY",
        ),
    )

    state = generate_state(
        snapshot=snapshot,
        rule=rule,
    )

    assert state.source_policy_ids == (
        "CP01-CONTEXTUAL-ADAPTATION",
        "CP02-BRAND-VISIBILITY",
    )


def test_generation_preserves_absence_of_policy_references() -> None:
    snapshot = create_snapshot()

    rule = create_rule(
        context_definition=(
            snapshot.context_definition
        ),
        source_policy_ids=(),
    )

    state = generate_state(
        snapshot=snapshot,
        rule=rule,
    )

    assert state.source_policy_ids == ()


def test_generation_rejects_invalid_rule() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "rule must be a "
            "RetailExpectedStateRule"
        ),
    ):
        generate_retail_expected_state(
            expected_state_id=(
                "GENERATED-EXPECTED-001"
            ),
            expected_state_version=1,
            rule="EXPECTED-RULE-001",
            snapshot=create_snapshot(),
        )


def test_generation_rejects_invalid_snapshot() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "snapshot must be a "
            "RetailContextSnapshot"
        ),
    ):
        generate_retail_expected_state(
            expected_state_id=(
                "GENERATED-EXPECTED-001"
            ),
            expected_state_version=1,
            rule=create_rule(),
            snapshot="SNAPSHOT-STORE-A",
        )


def test_generation_rejects_rule_from_different_customer() -> None:
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
        generate_state(
            snapshot=snapshot,
            rule=foreign_rule,
        )


def test_generation_rejects_missing_required_dimension() -> None:
    snapshot = create_snapshot()

    incomplete_snapshot = replace(
        snapshot,
        dimensions=(
            snapshot.dimensions[0],
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "expected state requires "
            "an applicable rule: "
            "INSUFFICIENT_EVIDENCE"
        ),
    ):
        generate_state(
            snapshot=incomplete_snapshot,
        )


def test_generation_rejects_insufficient_dimension_evidence() -> None:
    snapshot = create_snapshot()

    insufficient_inventory = create_dimension(
        dimension_id="DIM-INVENTORY-001",
        dimension_type="INVENTORY_STATE",
        value=None,
        evidence_status=(
            DimensionEvidenceStatus
            .INSUFFICIENT_EVIDENCE
        ),
    )

    insufficient_snapshot = replace(
        snapshot,
        dimensions=(
            snapshot.dimensions[0],
            insufficient_inventory,
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "expected state requires "
            "an applicable rule: "
            "INSUFFICIENT_EVIDENCE"
        ),
    ):
        generate_state(
            snapshot=(
                insufficient_snapshot
            ),
        )


def test_generation_rejects_disputed_dimension_evidence() -> None:
    snapshot = create_snapshot()

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

    with pytest.raises(
        ValueError,
        match=(
            "expected state requires "
            "an applicable rule: "
            "DISPUTED"
        ),
    ):
        generate_state(
            snapshot=(
                disputed_snapshot
            ),
        )


def test_generation_rejects_disputed_dimension_applicability() -> None:
    snapshot = create_snapshot()

    disputed_department = create_dimension(
        dimension_id="DIM-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
        value="GIRLS",
        applicability=(
            DimensionApplicability.DISPUTED
        ),
    )

    disputed_snapshot = replace(
        snapshot,
        dimensions=(
            disputed_department,
            snapshot.dimensions[1],
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "expected state requires "
            "an applicable rule: "
            "DISPUTED"
        ),
    ):
        generate_state(
            snapshot=(
                disputed_snapshot
            ),
        )


def test_generation_rejects_incompatible_dimension_value() -> None:
    snapshot = create_snapshot()

    incompatible_inventory = create_dimension(
        dimension_id="DIM-INVENTORY-001",
        dimension_type="INVENTORY_STATE",
        value="UNAVAILABLE",
    )

    incompatible_snapshot = replace(
        snapshot,
        dimensions=(
            snapshot.dimensions[0],
            incompatible_inventory,
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "expected state requires "
            "an applicable rule: "
            "NOT_APPLICABLE"
        ),
    ):
        generate_state(
            snapshot=(
                incompatible_snapshot
            ),
        )


def test_generation_allows_unrelated_disputed_dimension() -> None:
    snapshot = create_snapshot()

    disputed_inventory = create_dimension(
        dimension_id="DIM-INVENTORY-001",
        dimension_type="INVENTORY_STATE",
        value="AVAILABLE",
        evidence_status=(
            DimensionEvidenceStatus.DISPUTED
        ),
    )

    disputed_snapshot = replace(
        snapshot,
        dimensions=(
            snapshot.dimensions[0],
            disputed_inventory,
        ),
    )

    rule = create_rule(
        context_definition=(
            disputed_snapshot.context_definition
        ),
        required_dimension_values=(
            (
                "DEPARTMENT",
                "GIRLS",
            ),
        ),
    )

    state = generate_state(
        snapshot=(
            disputed_snapshot
        ),
        rule=rule,
    )

    assert state.source_dimension_ids == (
        "DIM-DEPARTMENT-001",
    )


def test_generation_preserves_distinct_customer_expectations() -> None:
    snapshot_a = create_snapshot()

    definition_b = create_definition(
        context_definition_id=(
            "DEFINITION-CUSTOMER-B"
        ),
        customer_id="CUSTOMER-B",
    )

    snapshot_b = replace(
        snapshot_a,
        snapshot_id=(
            "SNAPSHOT-STORE-B"
        ),
        context_definition=(
            definition_b
        ),
    )

    rule_a = create_rule(
        context_definition=(
            snapshot_a.context_definition
        ),
        expected_value="HERO",
    )

    rule_b = create_rule(
        expected_state_rule_id=(
            "EXPECTED-RULE-CUSTOMER-B"
        ),
        context_definition=(
            snapshot_b.context_definition
        ),
        expected_value="SUPPORT",
    )

    state_a = generate_state(
        expected_state_id=(
            "EXPECTED-STORE-A"
        ),
        snapshot=snapshot_a,
        rule=rule_a,
    )

    state_b = generate_state(
        expected_state_id=(
            "EXPECTED-STORE-B"
        ),
        snapshot=snapshot_b,
        rule=rule_b,
    )

    assert state_a.expected_value == (
        "HERO"
    )

    assert state_b.expected_value == (
        "SUPPORT"
    )

    assert (
        state_a.snapshot.context_definition.customer_id
        != state_b.snapshot.context_definition.customer_id
    )


def test_generated_expected_state_is_immutable() -> None:
    state = generate_state()

    with pytest.raises(
        FrozenInstanceError,
    ):
        state.expected_value = (
            "SUPPORT"
        )


def test_generation_does_not_mutate_snapshot_or_rule() -> None:
    snapshot = create_snapshot()

    rule = create_rule(
        context_definition=(
            snapshot.context_definition
        ),
    )

    original_dimensions = (
        snapshot.dimensions
    )

    original_conditions = (
        rule.required_dimension_values
    )

    original_policy_ids = (
        rule.source_policy_ids
    )

    generate_state(
        snapshot=snapshot,
        rule=rule,
    )

    assert snapshot.dimensions == (
        original_dimensions
    )

    assert rule.required_dimension_values == (
        original_conditions
    )

    assert rule.source_policy_ids == (
        original_policy_ids
    )


def test_generation_does_not_infer_recommendation_or_authority() -> None:
    state = generate_state()

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
