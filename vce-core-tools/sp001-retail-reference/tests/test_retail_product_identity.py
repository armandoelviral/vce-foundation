from dataclasses import FrozenInstanceError, fields, replace
import inspect

import pytest

from sp001.contracts.retail_product_identity import RetailProductIdentity


def create_identity(
    **overrides: object,
) -> RetailProductIdentity:
    values = {
        "product_id": "PRODUCT-001",
        "sku": "SKU-000123",
        "catalog_id": "CATALOG-MX-001",
        "catalog_version": 1,
    }
    values.update(overrides)
    return RetailProductIdentity(**values)


def test_product_identity_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(RetailProductIdentity)) == (
        "product_id",
        "sku",
        "catalog_id",
        "catalog_version",
    )


def test_product_identity_is_immutable() -> None:
    identity = create_identity()
    with pytest.raises(FrozenInstanceError):
        identity.sku = "SKU-999999"


def test_product_identity_uses_slots() -> None:
    assert not hasattr(create_identity(), "__dict__")


def test_product_identity_preserves_exact_declared_values() -> None:
    product_id = "Product-MX 001"
    sku = "Sku-00 0123"
    catalog_id = "Catalog-MX 2026"
    identity = create_identity(
        product_id=product_id,
        sku=sku,
        catalog_id=catalog_id,
        catalog_version=7,
    )
    assert identity.product_id is product_id
    assert identity.sku is sku
    assert identity.catalog_id is catalog_id
    assert identity.catalog_version == 7


def test_sku_preserves_leading_zeroes() -> None:
    identity = create_identity(sku="00000123")
    assert identity.sku == "00000123"


def test_sku_is_not_normalized_or_case_folded() -> None:
    first = create_identity(sku="Sku-AbC")
    second = create_identity(sku="SKU-ABC")
    assert first.sku == "Sku-AbC"
    assert second.sku == "SKU-ABC"
    assert first != second


def test_same_declared_identity_is_deterministically_equal() -> None:
    assert create_identity() == create_identity()


def test_different_catalog_versions_are_distinct_identities() -> None:
    first = create_identity(catalog_version=1)
    second = create_identity(catalog_version=2)
    assert first != second


def test_product_identity_is_hashable() -> None:
    first = create_identity()
    second = create_identity()
    assert {first, second} == {first}


@pytest.mark.parametrize(
    "field",
    (
        "product_id",
        "sku",
        "catalog_id",
    ),
)
@pytest.mark.parametrize(
    "value",
    (
        None,
        "",
        "   ",
        1,
        object(),
    ),
)
def test_identity_fields_require_nonempty_strings(
    field: str,
    value: object,
) -> None:
    with pytest.raises(ValueError, match=rf"{field} must not be empty"):
        create_identity(**{field: value})


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
def test_catalog_version_requires_strict_positive_integer(value: object) -> None:
    with pytest.raises(
        ValueError,
        match="catalog_version must be a positive integer",
    ):
        create_identity(catalog_version=value)


def test_catalog_version_accepts_positive_integer() -> None:
    identity = create_identity(catalog_version=999)
    assert identity.catalog_version == 999


def test_reconstruction_preserves_independent_product_and_sku_identity() -> None:
    original = create_identity()
    replacement = replace(original, sku="SKU-000124")
    assert replacement.product_id == original.product_id
    assert replacement.sku != original.sku


def test_contract_has_no_builder_or_lookup_side_effect() -> None:
    module = __import__(
        "sp001.contracts.retail_product_identity",
        fromlist=["*"],
    )
    functions = tuple(
        name
        for name, value in vars(module).items()
        if inspect.isfunction(value)
        and value.__module__ == module.__name__
    )
    assert functions == ()


def test_contract_has_no_inventory_geometry_or_commercial_fields() -> None:
    field_names = {field.name for field in fields(RetailProductIdentity)}
    assert field_names.isdisjoint(
        {
            "stock",
            "quantity",
            "point_of_sale_id",
            "height",
            "width",
            "depth",
            "rotation_class",
            "substitute_skus",
            "margin",
            "price",
            "currency",
        }
    )


def test_contract_adds_no_recommendation_authority_or_io_capability() -> None:
    module = __import__(
        "sp001.contracts.retail_product_identity",
        fromlist=["*"],
    )
    source = inspect.getsource(module).casefold()
    for forbidden in (
        "recommend",
        "priority",
        "penalty",
        "exemption",
        "authentic",
        "authority",
        "notion",
        "requests",
        "open(",
        "read_",
        "write_",
    ):
        assert forbidden not in source
