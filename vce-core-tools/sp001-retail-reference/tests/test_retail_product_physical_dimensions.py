from dataclasses import FrozenInstanceError, fields, replace
import inspect

import pytest

from sp001.contracts.retail_product_identity import RetailProductIdentity
from sp001.contracts.retail_product_physical_dimensions import (
    RetailProductPhysicalDimensions,
)


def create_identity() -> RetailProductIdentity:
    return RetailProductIdentity(
        product_id="PRODUCT-001",
        sku="SKU-000123",
        catalog_id="CATALOG-MX-001",
        catalog_version=1,
    )


def create_dimensions(
    **overrides: object,
) -> RetailProductPhysicalDimensions:
    values = {
        "product_identity": create_identity(),
        "height_millimeters": 250,
        "width_millimeters": 180,
        "depth_millimeters": 40,
    }
    values.update(overrides)
    return RetailProductPhysicalDimensions(**values)


def test_physical_dimension_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(RetailProductPhysicalDimensions)
    ) == (
        "product_identity",
        "height_millimeters",
        "width_millimeters",
        "depth_millimeters",
    )


def test_physical_dimensions_are_immutable() -> None:
    dimensions = create_dimensions()
    with pytest.raises(FrozenInstanceError):
        dimensions.height_millimeters = 300


def test_physical_dimensions_use_slots() -> None:
    assert not hasattr(create_dimensions(), "__dict__")


def test_physical_dimensions_preserve_exact_product_reference() -> None:
    identity = create_identity()
    dimensions = create_dimensions(product_identity=identity)
    assert dimensions.product_identity is identity


def test_physical_dimensions_preserve_exact_measurements() -> None:
    dimensions = create_dimensions(
        height_millimeters=251,
        width_millimeters=179,
        depth_millimeters=41,
    )
    assert dimensions.height_millimeters == 251
    assert dimensions.width_millimeters == 179
    assert dimensions.depth_millimeters == 41


def test_minimum_positive_measurements_are_accepted() -> None:
    dimensions = create_dimensions(
        height_millimeters=1,
        width_millimeters=1,
        depth_millimeters=1,
    )
    assert (
        dimensions.height_millimeters,
        dimensions.width_millimeters,
        dimensions.depth_millimeters,
    ) == (1, 1, 1)


def test_same_declared_dimensions_are_deterministically_equal() -> None:
    assert create_dimensions() == create_dimensions()


def test_different_measurements_are_distinct() -> None:
    assert create_dimensions() != create_dimensions(depth_millimeters=41)


def test_physical_dimensions_are_hashable() -> None:
    first = create_dimensions()
    second = create_dimensions()
    assert {first, second} == {first}


@pytest.mark.parametrize(
    "value",
    (
        None,
        "PRODUCT-001",
        object(),
    ),
)
def test_product_identity_requires_exact_type(value: object) -> None:
    with pytest.raises(
        TypeError,
        match="product_identity must be a RetailProductIdentity",
    ):
        create_dimensions(product_identity=value)


@pytest.mark.parametrize(
    "field",
    (
        "height_millimeters",
        "width_millimeters",
        "depth_millimeters",
    ),
)
@pytest.mark.parametrize(
    "value",
    (
        None,
        True,
        False,
        0,
        -1,
        1.0,
        "1",
        object(),
    ),
)
def test_measurements_require_strict_positive_integers(
    field: str,
    value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=rf"{field} must be a positive integer",
    ):
        create_dimensions(**{field: value})


def test_replacement_preserves_other_declared_facts() -> None:
    original = create_dimensions()
    changed = replace(original, width_millimeters=181)
    assert changed.product_identity is original.product_identity
    assert changed.height_millimeters == original.height_millimeters
    assert changed.depth_millimeters == original.depth_millimeters
    assert changed.width_millimeters == 181


def test_contract_exposes_no_derived_volume_fit_or_orientation() -> None:
    dimensions = create_dimensions()
    for forbidden in (
        "volume",
        "fits",
        "orientation",
        "facing_capacity",
    ):
        assert not hasattr(dimensions, forbidden)


def test_contract_has_no_builder_conversion_or_side_effect() -> None:
    module = __import__(
        "sp001.contracts.retail_product_physical_dimensions",
        fromlist=["*"],
    )
    functions = tuple(
        name
        for name, value in vars(module).items()
        if inspect.isfunction(value)
        and value.__module__ == module.__name__
    )
    assert functions == ()


def test_contract_adds_no_inventory_commercial_or_io_capability() -> None:
    module = __import__(
        "sp001.contracts.retail_product_physical_dimensions",
        fromlist=["*"],
    )
    source = inspect.getsource(module).casefold()
    for forbidden in (
        "stock",
        "inventory",
        "rotation",
        "substitute",
        "margin",
        "price",
        "recommend",
        "priority",
        "notion",
        "requests",
        "open(",
        "read_",
        "write_",
    ):
        assert forbidden not in source
