from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.retail_context_definition import (
    RetailContextDefinition,
)


def create_definition(
    **overrides,
) -> RetailContextDefinition:
    values = {
        "context_definition_id": "CTX-DEFINITION-001",
        "customer_id": "CUSTOMER-PSEUDONYM-001",
        "definition_version": 1,
        "dimension_types": (
            "FLOOR_AREA",
            "DEPARTMENT",
            "FIXTURE_TYPE",
        ),
    }

    values.update(
        overrides,
    )

    return RetailContextDefinition(
        **values,
    )


def test_definition_preserves_explicit_identity() -> None:
    definition = create_definition()

    assert definition.context_definition_id == (
        "CTX-DEFINITION-001"
    )


def test_definition_preserves_opaque_customer_identity() -> None:
    definition = create_definition()

    assert definition.customer_id == (
        "CUSTOMER-PSEUDONYM-001"
    )


def test_definition_preserves_explicit_version() -> None:
    definition = create_definition()

    assert definition.definition_version == 1


def test_definition_preserves_customer_declared_dimension_types() -> None:
    definition = create_definition()

    assert definition.dimension_types == (
        "FLOOR_AREA",
        "DEPARTMENT",
        "FIXTURE_TYPE",
    )


def test_definition_accepts_customer_defined_dimension_type() -> None:
    definition = create_definition(
        dimension_types=(
            "CUSTOMER_DEFINED_COMMERCIAL_ZONE",
            "CUSTOMER_DEFINED_SEASON_WINDOW",
        ),
    )

    assert definition.dimension_types == (
        "CUSTOMER_DEFINED_COMMERCIAL_ZONE",
        "CUSTOMER_DEFINED_SEASON_WINDOW",
    )


def test_distinct_customers_can_declare_distinct_dimension_sets() -> None:
    first = create_definition(
        context_definition_id="CTX-DEFINITION-001",
        customer_id="CUSTOMER-PSEUDONYM-001",
        dimension_types=(
            "FLOOR_AREA",
            "FIXTURE_TYPE",
        ),
    )

    second = create_definition(
        context_definition_id="CTX-DEFINITION-002",
        customer_id="CUSTOMER-PSEUDONYM-002",
        dimension_types=(
            "COMMERCIAL_CLUSTER",
            "CUSTOMER_DEFINED_LOCAL_PRIORITY",
        ),
    )

    assert first.customer_id != second.customer_id

    assert first.dimension_types != (
        second.dimension_types
    )


def test_distinct_definition_versions_remain_distinct() -> None:
    first = create_definition(
        definition_version=1,
        dimension_types=(
            "DEPARTMENT",
        ),
    )

    second = create_definition(
        definition_version=2,
        dimension_types=(
            "DEPARTMENT",
            "PURCHASE_VOLUME",
        ),
    )

    assert first.context_definition_id == (
        second.context_definition_id
    )

    assert first.definition_version == 1
    assert second.definition_version == 2
    assert first != second


def test_definition_is_immutable() -> None:
    definition = create_definition()

    with pytest.raises(
        FrozenInstanceError,
    ):
        definition.customer_id = (
            "CUSTOMER-PSEUDONYM-002"
        )


def test_definition_rejects_mutable_dimension_collection() -> None:
    with pytest.raises(
        TypeError,
        match="dimension_types must be an immutable tuple",
    ):
        create_definition(
            dimension_types=[
                "FLOOR_AREA",
                "DEPARTMENT",
            ],
        )


def test_definition_rejects_empty_dimension_collection() -> None:
    with pytest.raises(
        ValueError,
        match="dimension_types must not be empty",
    ):
        create_definition(
            dimension_types=(),
        )


@pytest.mark.parametrize(
    "identity",
    (
        "",
        "   ",
        123,
        None,
    ),
)
def test_definition_rejects_invalid_definition_identity(
    identity,
) -> None:
    with pytest.raises(
        ValueError,
        match="context_definition_id must not be empty",
    ):
        create_definition(
            context_definition_id=identity,
        )


@pytest.mark.parametrize(
    "identity",
    (
        "",
        "   ",
        123,
        None,
    ),
)
def test_definition_rejects_invalid_customer_identity(
    identity,
) -> None:
    with pytest.raises(
        ValueError,
        match="customer_id must not be empty",
    ):
        create_definition(
            customer_id=identity,
        )


@pytest.mark.parametrize(
    "version",
    (
        0,
        -1,
        True,
        False,
        "1",
        None,
    ),
)
def test_definition_rejects_invalid_version(
    version,
) -> None:
    with pytest.raises(
        ValueError,
        match="definition_version must be a positive integer",
    ):
        create_definition(
            definition_version=version,
        )


@pytest.mark.parametrize(
    "dimension_type",
    (
        "",
        "   ",
        123,
        None,
    ),
)
def test_definition_rejects_invalid_dimension_type(
    dimension_type,
) -> None:
    with pytest.raises(
        ValueError,
        match="dimension_type must not be empty",
    ):
        create_definition(
            dimension_types=(
                "DEPARTMENT",
                dimension_type,
            ),
        )


def test_definition_rejects_duplicate_dimension_type() -> None:
    with pytest.raises(
        ValueError,
        match="duplicate dimension_type: DEPARTMENT",
    ):
        create_definition(
            dimension_types=(
                "DEPARTMENT",
                "FIXTURE_TYPE",
                "DEPARTMENT",
            ),
        )


def test_definition_preserves_declared_dimension_order() -> None:
    dimension_types = (
        "COMMERCIAL_CLUSTER",
        "PURCHASE_VOLUME",
        "DEPARTMENT",
    )

    definition = create_definition(
        dimension_types=dimension_types,
    )

    assert definition.dimension_types == (
        dimension_types
    )


def test_definition_does_not_impose_universal_dimensions() -> None:
    definition = create_definition(
        dimension_types=(
            "CUSTOMER_DEFINED_OPERATIONAL_REQUIREMENT",
        ),
    )

    assert definition.dimension_types == (
        "CUSTOMER_DEFINED_OPERATIONAL_REQUIREMENT",
    )

    assert "FLOOR_AREA" not in (
        definition.dimension_types
    )

    assert "FIXTURE_TYPE" not in (
        definition.dimension_types
    )


def test_definition_does_not_infer_store_scope_or_authority() -> None:
    definition = create_definition()

    assert not hasattr(
        definition,
        "point_of_sale_id",
    )

    assert not hasattr(
        definition,
        "department_id",
    )

    assert not hasattr(
        definition,
        "authority",
    )

    assert not hasattr(
        definition,
        "owner",
    )
