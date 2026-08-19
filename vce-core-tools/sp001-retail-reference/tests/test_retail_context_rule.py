from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.retail_context_rule import (
    RetailContextRule,
)


def test_rule_preserves_identity_and_type() -> None:
    rule = RetailContextRule(
        rule_id="RULE-FIXTURE-001",
        rule_type="VERIFY_FIXTURE_PRESENTATION",
        required_dimension_ids=(
            "CTX-DEPARTMENT-001",
            "CTX-FIXTURE-001",
        ),
    )

    assert rule.rule_id == "RULE-FIXTURE-001"

    assert (
        rule.rule_type
        == "VERIFY_FIXTURE_PRESENTATION"
    )


def test_rule_preserves_declared_context_dependencies() -> None:
    rule = RetailContextRule(
        rule_id="RULE-FIXTURE-001",
        rule_type="VERIFY_FIXTURE_PRESENTATION",
        required_dimension_ids=(
            "CTX-DEPARTMENT-001",
            "CTX-FIXTURE-001",
        ),
    )

    assert rule.required_dimension_ids == (
        "CTX-DEPARTMENT-001",
        "CTX-FIXTURE-001",
    )


def test_customer_defined_rule_type_remains_supported() -> None:
    rule = RetailContextRule(
        rule_id="RULE-CUSTOM-001",
        rule_type="CUSTOMER_DEFINED_PRESENTATION_STANDARD",
        required_dimension_ids=(
            "CTX-CUSTOM-001",
        ),
    )

    assert (
        rule.rule_type
        == "CUSTOMER_DEFINED_PRESENTATION_STANDARD"
    )


def test_rule_is_immutable() -> None:
    rule = RetailContextRule(
        rule_id="RULE-FIXTURE-001",
        rule_type="VERIFY_FIXTURE_PRESENTATION",
        required_dimension_ids=(
            "CTX-FIXTURE-001",
        ),
    )

    with pytest.raises(FrozenInstanceError):
        rule.rule_id = "RULE-FIXTURE-002"


def test_rule_dependency_collection_is_immutable() -> None:
    rule = RetailContextRule(
        rule_id="RULE-FIXTURE-001",
        rule_type="VERIFY_FIXTURE_PRESENTATION",
        required_dimension_ids=(
            "CTX-FIXTURE-001",
        ),
    )

    with pytest.raises(TypeError):
        rule.required_dimension_ids[0] = (
            "CTX-FIXTURE-002"
        )


@pytest.mark.parametrize(
    "invalid_rule_id",
    ("", "   "),
)
def test_rule_rejects_empty_identity(
    invalid_rule_id: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="rule_id must not be empty",
    ):
        RetailContextRule(
            rule_id=invalid_rule_id,
            rule_type="VERIFY_FIXTURE_PRESENTATION",
            required_dimension_ids=(
                "CTX-FIXTURE-001",
            ),
        )


@pytest.mark.parametrize(
    "invalid_rule_type",
    ("", "   "),
)
def test_rule_rejects_empty_type(
    invalid_rule_type: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="rule_type must not be empty",
    ):
        RetailContextRule(
            rule_id="RULE-FIXTURE-001",
            rule_type=invalid_rule_type,
            required_dimension_ids=(
                "CTX-FIXTURE-001",
            ),
        )


def test_rule_rejects_mutable_dependency_collection() -> None:
    with pytest.raises(
        TypeError,
        match="required_dimension_ids must be an immutable tuple",
    ):
        RetailContextRule(
            rule_id="RULE-FIXTURE-001",
            rule_type="VERIFY_FIXTURE_PRESENTATION",
            required_dimension_ids=[
                "CTX-FIXTURE-001",
            ],
        )


def test_rule_rejects_empty_dependency_collection() -> None:
    with pytest.raises(
        ValueError,
        match="required_dimension_ids must not be empty",
    ):
        RetailContextRule(
            rule_id="RULE-FIXTURE-001",
            rule_type="VERIFY_FIXTURE_PRESENTATION",
            required_dimension_ids=(),
        )


@pytest.mark.parametrize(
    "invalid_dimension_id",
    ("", "   "),
)
def test_rule_rejects_empty_dimension_identity(
    invalid_dimension_id: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="required dimension_id must not be empty",
    ):
        RetailContextRule(
            rule_id="RULE-FIXTURE-001",
            rule_type="VERIFY_FIXTURE_PRESENTATION",
            required_dimension_ids=(
                invalid_dimension_id,
            ),
        )


def test_rule_rejects_non_string_dimension_identity() -> None:
    with pytest.raises(
        ValueError,
        match="required dimension_id must not be empty",
    ):
        RetailContextRule(
            rule_id="RULE-FIXTURE-001",
            rule_type="VERIFY_FIXTURE_PRESENTATION",
            required_dimension_ids=(
                123,
            ),
        )


def test_rule_rejects_duplicate_dimension_identity() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "duplicate required dimension_id: "
            "CTX-FIXTURE-001"
        ),
    ):
        RetailContextRule(
            rule_id="RULE-FIXTURE-001",
            rule_type="VERIFY_FIXTURE_PRESENTATION",
            required_dimension_ids=(
                "CTX-FIXTURE-001",
                "CTX-FIXTURE-001",
            ),
        )


def test_rule_preserves_customer_declared_dependency_order() -> None:
    rule = RetailContextRule(
        rule_id="RULE-FIXTURE-001",
        rule_type="VERIFY_FIXTURE_PRESENTATION",
        required_dimension_ids=(
            "CTX-FIXTURE-002",
            "CTX-DEPARTMENT-001",
            "CTX-FIXTURE-001",
        ),
    )

    assert rule.required_dimension_ids == (
        "CTX-FIXTURE-002",
        "CTX-DEPARTMENT-001",
        "CTX-FIXTURE-001",
    )
