from dataclasses import (
    FrozenInstanceError,
    fields,
)

import pytest

from sp001.contracts.retail_context_definition import (
    RetailContextDefinition,
)
from sp001.contracts.retail_expected_state_rule import (
    RetailExpectedStateRule,
)


def create_definition(
    *,
    context_definition_id: str = "DEFINITION-CUSTOMER-A",
    customer_id: str = "CUSTOMER-A",
    definition_version: int = 1,
    dimension_types: tuple[str, ...] = (
        "DEPARTMENT",
        "INVENTORY_STATE",
        "SEASON_WINDOW",
    ),
) -> RetailContextDefinition:
    return RetailContextDefinition(
        context_definition_id=context_definition_id,
        customer_id=customer_id,
        definition_version=definition_version,
        dimension_types=dimension_types,
    )


def create_rule(
    *,
    expected_state_rule_id: str = "EXPECTED-RULE-001",
    expected_state_rule_version: int = 1,
    context_definition: RetailContextDefinition | None = None,
    expectation_type: str = "VISIBILITY_PRIORITY",
    expected_value: str = "HERO",
    required_dimension_values: tuple[
        tuple[str, str],
        ...,
    ] = (
        (
            "DEPARTMENT",
            "GIRLS",
        ),
        (
            "INVENTORY_STATE",
            "AVAILABLE",
        ),
    ),
    source_policy_ids: tuple[str, ...] = (
        "CP01-CONTEXTUAL-ADAPTATION",
    ),
) -> RetailExpectedStateRule:
    return RetailExpectedStateRule(
        expected_state_rule_id=expected_state_rule_id,
        expected_state_rule_version=(
            expected_state_rule_version
        ),
        context_definition=(
            context_definition
            if context_definition is not None
            else create_definition()
        ),
        expectation_type=expectation_type,
        expected_value=expected_value,
        required_dimension_values=(
            required_dimension_values
        ),
        source_policy_ids=source_policy_ids,
    )


def test_rule_declares_exact_customer_configuration_contract() -> None:
    assert tuple(
        field.name
        for field in fields(
            RetailExpectedStateRule,
        )
    ) == (
        "expected_state_rule_id",
        "expected_state_rule_version",
        "context_definition",
        "expectation_type",
        "expected_value",
        "required_dimension_values",
        "source_policy_ids",
    )


def test_rule_preserves_explicit_identity() -> None:
    rule = create_rule()

    assert rule.expected_state_rule_id == (
        "EXPECTED-RULE-001"
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
def test_rule_rejects_invalid_identity(
    invalid_identity: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "expected_state_rule_id "
            "must not be empty"
        ),
    ):
        create_rule(
            expected_state_rule_id=invalid_identity,
        )


def test_rule_preserves_positive_version() -> None:
    rule = create_rule(
        expected_state_rule_version=3,
    )

    assert rule.expected_state_rule_version == 3


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
def test_rule_rejects_invalid_version(
    invalid_version: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "expected_state_rule_version "
            "must be a positive integer"
        ),
    ):
        create_rule(
            expected_state_rule_version=(
                invalid_version
            ),
        )


def test_rule_preserves_customer_definition_identity() -> None:
    definition = create_definition(
        context_definition_id=(
            "DEFINITION-CUSTOMER-B"
        ),
        customer_id="CUSTOMER-B",
        definition_version=4,
    )

    rule = create_rule(
        context_definition=definition,
    )

    assert rule.context_definition is definition

    assert rule.context_definition.customer_id == (
        "CUSTOMER-B"
    )

    assert (
        rule.context_definition.definition_version
        == 4
    )


@pytest.mark.parametrize(
    "invalid_definition",
    (
        None,
        "DEFINITION-CUSTOMER-A",
        123,
        {},
    ),
)
def test_rule_rejects_invalid_customer_definition(
    invalid_definition: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "context_definition must be a "
            "RetailContextDefinition"
        ),
    ):
        RetailExpectedStateRule(
            expected_state_rule_id=(
                "EXPECTED-RULE-001"
            ),
            expected_state_rule_version=1,
            context_definition=(
                invalid_definition
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
            ),
        )


def test_rule_preserves_customer_defined_expectation_type() -> None:
    rule = create_rule(
        expectation_type=(
            "CUSTOMER_DEFINED_WINDOW_PRIORITY"
        ),
    )

    assert rule.expectation_type == (
        "CUSTOMER_DEFINED_WINDOW_PRIORITY"
    )


@pytest.mark.parametrize(
    "invalid_expectation_type",
    (
        "",
        "   ",
        None,
        123,
    ),
)
def test_rule_rejects_invalid_expectation_type(
    invalid_expectation_type: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "expectation_type "
            "must not be empty"
        ),
    ):
        create_rule(
            expectation_type=(
                invalid_expectation_type
            ),
        )


def test_rule_preserves_explicit_expected_value() -> None:
    rule = create_rule(
        expected_value="SUPPORT",
    )

    assert rule.expected_value == "SUPPORT"


@pytest.mark.parametrize(
    "invalid_expected_value",
    (
        "",
        "   ",
        None,
        123,
    ),
)
def test_rule_rejects_invalid_expected_value(
    invalid_expected_value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "expected_value "
            "must not be empty"
        ),
    ):
        create_rule(
            expected_value=invalid_expected_value,
        )


def test_rule_preserves_immutable_dimension_conditions() -> None:
    rule = create_rule()

    assert rule.required_dimension_values == (
        (
            "DEPARTMENT",
            "GIRLS",
        ),
        (
            "INVENTORY_STATE",
            "AVAILABLE",
        ),
    )


def test_rule_rejects_mutable_dimension_conditions() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "required_dimension_values "
            "must be an immutable tuple"
        ),
    ):
        create_rule(
            required_dimension_values=[
                (
                    "DEPARTMENT",
                    "GIRLS",
                ),
            ],
        )


def test_rule_rejects_empty_dimension_conditions() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "required_dimension_values "
            "must not be empty"
        ),
    ):
        create_rule(
            required_dimension_values=(),
        )


@pytest.mark.parametrize(
    "invalid_condition",
    (
        "DEPARTMENT",
        (
            "DEPARTMENT",
        ),
        (
            "DEPARTMENT",
            "GIRLS",
            "EXTRA",
        ),
        [
            "DEPARTMENT",
            "GIRLS",
        ],
    ),
)
def test_rule_rejects_invalid_dimension_condition_shape(
    invalid_condition: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "dimension condition must be "
            "an immutable type-value pair"
        ),
    ):
        create_rule(
            required_dimension_values=(
                invalid_condition,
            ),
        )


@pytest.mark.parametrize(
    "invalid_dimension_type",
    (
        "",
        "   ",
        None,
        123,
    ),
)
def test_rule_rejects_invalid_condition_dimension_type(
    invalid_dimension_type: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "condition dimension_type "
            "must not be empty"
        ),
    ):
        create_rule(
            required_dimension_values=(
                (
                    invalid_dimension_type,
                    "GIRLS",
                ),
            ),
        )


@pytest.mark.parametrize(
    "invalid_dimension_value",
    (
        "",
        "   ",
        None,
        123,
    ),
)
def test_rule_rejects_invalid_condition_dimension_value(
    invalid_dimension_value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "condition dimension_value "
            "must not be empty"
        ),
    ):
        create_rule(
            required_dimension_values=(
                (
                    "DEPARTMENT",
                    invalid_dimension_value,
                ),
            ),
        )


def test_rule_rejects_undeclared_customer_dimension_type() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "undeclared condition dimension_type: "
            "PROMOTION_STATE"
        ),
    ):
        create_rule(
            required_dimension_values=(
                (
                    "PROMOTION_STATE",
                    "ACTIVE",
                ),
            ),
        )


def test_rule_rejects_duplicate_condition_dimension_type() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "duplicate condition dimension_type: "
            "DEPARTMENT"
        ),
    ):
        create_rule(
            required_dimension_values=(
                (
                    "DEPARTMENT",
                    "GIRLS",
                ),
                (
                    "DEPARTMENT",
                    "BOYS",
                ),
            ),
        )


def test_rule_preserves_declared_condition_order() -> None:
    rule = create_rule(
        required_dimension_values=(
            (
                "SEASON_WINDOW",
                "ACTIVE",
            ),
            (
                "DEPARTMENT",
                "GIRLS",
            ),
        ),
    )

    assert rule.required_dimension_values == (
        (
            "SEASON_WINDOW",
            "ACTIVE",
        ),
        (
            "DEPARTMENT",
            "GIRLS",
        ),
    )


def test_rule_preserves_optional_policy_references() -> None:
    rule = RetailExpectedStateRule(
        expected_state_rule_id=(
            "EXPECTED-RULE-001"
        ),
        expected_state_rule_version=1,
        context_definition=create_definition(),
        expectation_type=(
            "VISIBILITY_PRIORITY"
        ),
        expected_value="HERO",
        required_dimension_values=(
            (
                "DEPARTMENT",
                "GIRLS",
            ),
        ),
    )

    assert rule.source_policy_ids == ()


def test_rule_rejects_mutable_policy_references() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "source_policy_ids "
            "must be an immutable tuple"
        ),
    ):
        create_rule(
            source_policy_ids=[
                "CP01",
            ],
        )


@pytest.mark.parametrize(
    "invalid_policy_id",
    (
        "",
        "   ",
        None,
        123,
    ),
)
def test_rule_rejects_invalid_policy_reference(
    invalid_policy_id: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "source policy_id "
            "must not be empty"
        ),
    ):
        create_rule(
            source_policy_ids=(
                invalid_policy_id,
            ),
        )


def test_rule_rejects_duplicate_policy_references() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "duplicate source policy_id: "
            "CP01"
        ),
    ):
        create_rule(
            source_policy_ids=(
                "CP01",
                "CP01",
            ),
        )


def test_rule_is_immutable() -> None:
    rule = create_rule()

    with pytest.raises(
        FrozenInstanceError,
    ):
        rule.expected_value = "SUPPORT"


def test_customers_can_declare_different_expectations() -> None:
    customer_a_rule = create_rule(
        expected_state_rule_id=(
            "EXPECTED-RULE-CUSTOMER-A"
        ),
        context_definition=create_definition(
            context_definition_id=(
                "DEFINITION-CUSTOMER-A"
            ),
            customer_id="CUSTOMER-A",
        ),
        expected_value="HERO",
    )

    customer_b_rule = create_rule(
        expected_state_rule_id=(
            "EXPECTED-RULE-CUSTOMER-B"
        ),
        context_definition=create_definition(
            context_definition_id=(
                "DEFINITION-CUSTOMER-B"
            ),
            customer_id="CUSTOMER-B",
        ),
        expected_value="SUPPORT",
    )

    assert (
        customer_a_rule.required_dimension_values
        == customer_b_rule.required_dimension_values
    )

    assert customer_a_rule.expected_value == (
        "HERO"
    )

    assert customer_b_rule.expected_value == (
        "SUPPORT"
    )

    assert (
        customer_a_rule.context_definition.customer_id
        != customer_b_rule.context_definition.customer_id
    )


def test_rule_does_not_infer_execution_or_authority() -> None:
    rule = create_rule()

    for attribute in (
        "snapshot",
        "snapshot_id",
        "point_of_sale_id",
        "sku_id",
        "fixture_id",
        "facing_count",
        "compliance_status",
        "recommendation",
        "authority",
        "owner",
        "valid_from",
        "valid_until",
    ):
        assert not hasattr(
            rule,
            attribute,
        )
