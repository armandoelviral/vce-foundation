from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.contracts.retail_context_definition import (
    RetailContextDefinition,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)


def create_definition(
    *,
    context_definition_id: str = "RCP-DEFINITION-001",
    customer_id: str = "CUSTOMER-001",
    definition_version: int = 1,
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


def test_historical_definition_preserves_empty_requirement_metadata() -> None:
    definition = RetailContextDefinition(
        context_definition_id="RCP-DEFINITION-HISTORICAL",
        customer_id="CUSTOMER-001",
        definition_version=1,
        dimension_types=(
            "DEPARTMENT",
            "INVENTORY_STATE",
        ),
    )

    assert definition.dimension_types == (
        "DEPARTMENT",
        "INVENTORY_STATE",
    )
    assert definition.required_dimension_types == ()
    assert definition.optional_dimension_types == ()


def test_definition_appends_requirement_fields() -> None:
    assert tuple(
        field.name
        for field in fields(
            RetailContextDefinition,
        )
    ) == (
        "context_definition_id",
        "customer_id",
        "definition_version",
        "dimension_types",
        "required_dimension_types",
        "optional_dimension_types",
    )


def test_definition_accepts_complete_required_optional_partition() -> None:
    definition = create_definition()

    assert definition.required_dimension_types == (
        "DEPARTMENT",
        "INVENTORY_STATE",
    )
    assert definition.optional_dimension_types == (
        "PRESENTATION_CAPACITY",
    )


def test_customer_defined_vocabulary_remains_open() -> None:
    definition = create_definition(
        dimension_types=(
            "CUSTOMER_TRAFFIC_SIGNAL",
            "LOCAL_CREATIVE_BOUNDARY",
        ),
        required_dimension_types=(
            "CUSTOMER_TRAFFIC_SIGNAL",
        ),
        optional_dimension_types=(
            "LOCAL_CREATIVE_BOUNDARY",
        ),
    )

    assert definition.required_dimension_types == (
        "CUSTOMER_TRAFFIC_SIGNAL",
    )
    assert definition.optional_dimension_types == (
        "LOCAL_CREATIVE_BOUNDARY",
    )


def test_required_dimension_types_must_be_immutable_tuple() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "required_dimension_types must be "
            "an immutable tuple"
        ),
    ):
        create_definition(
            required_dimension_types=[
                "DEPARTMENT",
                "INVENTORY_STATE",
            ],
        )


def test_optional_dimension_types_must_be_immutable_tuple() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "optional_dimension_types must be "
            "an immutable tuple"
        ),
    ):
        create_definition(
            optional_dimension_types=[
                "PRESENTATION_CAPACITY",
            ],
        )


@pytest.mark.parametrize(
    "invalid_dimension_type",
    (
        "",
        "   ",
        None,
        7,
    ),
)
def test_required_dimension_type_must_be_nonempty_string(
    invalid_dimension_type: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="required dimension_type must not be empty",
    ):
        create_definition(
            required_dimension_types=(
                "DEPARTMENT",
                invalid_dimension_type,
            ),
        )


@pytest.mark.parametrize(
    "invalid_dimension_type",
    (
        "",
        "   ",
        None,
        7,
    ),
)
def test_optional_dimension_type_must_be_nonempty_string(
    invalid_dimension_type: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="optional dimension_type must not be empty",
    ):
        create_definition(
            optional_dimension_types=(
                invalid_dimension_type,
            ),
        )


def test_duplicate_required_dimension_type_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="duplicate required dimension_type: DEPARTMENT",
    ):
        create_definition(
            required_dimension_types=(
                "DEPARTMENT",
                "DEPARTMENT",
                "INVENTORY_STATE",
            ),
        )


def test_duplicate_optional_dimension_type_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "duplicate optional dimension_type: "
            "PRESENTATION_CAPACITY"
        ),
    ):
        create_definition(
            optional_dimension_types=(
                "PRESENTATION_CAPACITY",
                "PRESENTATION_CAPACITY",
            ),
        )


def test_undeclared_required_dimension_type_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="undeclared required dimension_type: SALES_STATE",
    ):
        create_definition(
            required_dimension_types=(
                "DEPARTMENT",
                "INVENTORY_STATE",
                "SALES_STATE",
            ),
        )


def test_undeclared_optional_dimension_type_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="undeclared optional dimension_type: SALES_STATE",
    ):
        create_definition(
            optional_dimension_types=(
                "PRESENTATION_CAPACITY",
                "SALES_STATE",
            ),
        )


def test_dimension_type_cannot_be_required_and_optional() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "dimension_type cannot be both required "
            "and optional: INVENTORY_STATE"
        ),
    ):
        create_definition(
            optional_dimension_types=(
                "INVENTORY_STATE",
                "PRESENTATION_CAPACITY",
            ),
        )


def test_configured_requirements_must_classify_every_dimension_type() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "dimension requirements must classify every "
            "dimension_type: PRESENTATION_CAPACITY"
        ),
    ):
        create_definition(
            required_dimension_types=(
                "DEPARTMENT",
                "INVENTORY_STATE",
            ),
            optional_dimension_types=(),
        )


def test_missing_required_dimension_does_not_invalidate_snapshot() -> None:
    definition = create_definition()

    snapshot = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
        context_definition=definition,
        dimensions=(),
    )

    assert snapshot.dimensions == ()
    assert snapshot.context_definition is definition


def test_definition_does_not_synthesize_missing_dimensions() -> None:
    definition = create_definition()

    assert not hasattr(
        definition,
        "missing_dimensions",
    )
    assert not hasattr(
        definition,
        "synthesized_dimensions",
    )
    assert not hasattr(
        definition,
        "completeness_status",
    )


def test_definition_versions_can_change_requirement_classification() -> None:
    first = create_definition(
        definition_version=1,
        required_dimension_types=(
            "DEPARTMENT",
            "INVENTORY_STATE",
        ),
        optional_dimension_types=(
            "PRESENTATION_CAPACITY",
        ),
    )

    second = create_definition(
        context_definition_id="RCP-DEFINITION-002",
        definition_version=2,
        required_dimension_types=(
            "DEPARTMENT",
        ),
        optional_dimension_types=(
            "INVENTORY_STATE",
            "PRESENTATION_CAPACITY",
        ),
    )

    assert first.required_dimension_types != (
        second.required_dimension_types
    )
    assert first.dimension_types == second.dimension_types


def test_requirement_configuration_is_immutable() -> None:
    definition = create_definition()

    with pytest.raises(
        FrozenInstanceError,
    ):
        definition.required_dimension_types = (
            "DEPARTMENT",
        )
