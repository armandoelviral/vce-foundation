from dataclasses import FrozenInstanceError, fields, replace
import inspect

import pytest

from sp001.contracts.retail_product_identity import RetailProductIdentity
from sp001.contracts.retail_product_rotation_classification import (
    RetailProductDeclaredRotationClassification,
    RetailProductRotationClass,
)


def identity() -> RetailProductIdentity:
    return RetailProductIdentity("PRODUCT-001", "SKU-001", "CATALOG-001", 1)


def classification(**changes: object) -> RetailProductDeclaredRotationClassification:
    values = dict(
        product_identity=identity(),
        rotation_class=RetailProductRotationClass.A,
        classification_scheme_id="ABC-SCHEME-001",
        classification_scheme_version=1,
    )
    values.update(changes)
    return RetailProductDeclaredRotationClassification(**values)


def test_rotation_vocabulary_is_exact() -> None:
    assert tuple(RetailProductRotationClass) == (
        RetailProductRotationClass.A,
        RetailProductRotationClass.B,
        RetailProductRotationClass.C,
    )
    assert tuple(item.value for item in RetailProductRotationClass) == ("A", "B", "C")


def test_classification_fields_are_exact() -> None:
    assert tuple(
        field.name for field in fields(RetailProductDeclaredRotationClassification)
    ) == (
        "product_identity",
        "rotation_class",
        "classification_scheme_id",
        "classification_scheme_version",
    )


def test_classification_is_frozen_slotted_and_hashable() -> None:
    value = classification()
    assert not hasattr(value, "__dict__")
    assert hash(value) == hash(classification())
    with pytest.raises(FrozenInstanceError):
        value.rotation_class = RetailProductRotationClass.B


def test_exact_product_and_scheme_facts_are_preserved() -> None:
    product = identity()
    scheme_id = "Abc Scheme-MX 001"
    value = classification(
        product_identity=product,
        classification_scheme_id=scheme_id,
        classification_scheme_version=7,
    )
    assert value.product_identity is product
    assert value.classification_scheme_id is scheme_id
    assert value.classification_scheme_version == 7


@pytest.mark.parametrize("rotation_class", tuple(RetailProductRotationClass))
def test_each_rotation_class_is_preserved(rotation_class) -> None:
    assert classification(rotation_class=rotation_class).rotation_class is rotation_class


@pytest.mark.parametrize("value", (None, "PRODUCT-001", object()))
def test_product_identity_requires_exact_type(value) -> None:
    with pytest.raises(TypeError, match="product_identity must be a RetailProductIdentity"):
        classification(product_identity=value)


@pytest.mark.parametrize("value", (None, "A", "HIGH", 1, object()))
def test_rotation_class_requires_exact_enum(value) -> None:
    with pytest.raises(TypeError, match="rotation_class must be a RetailProductRotationClass"):
        classification(rotation_class=value)


@pytest.mark.parametrize("value", (None, "", "   ", 1, object()))
def test_scheme_id_requires_nonempty_string(value) -> None:
    with pytest.raises(ValueError, match="classification_scheme_id must not be empty"):
        classification(classification_scheme_id=value)


@pytest.mark.parametrize("value", (None, True, False, 0, -1, 1.0, "1", object()))
def test_scheme_version_requires_strict_positive_integer(value) -> None:
    with pytest.raises(
        ValueError,
        match="classification_scheme_version must be a positive integer",
    ):
        classification(classification_scheme_version=value)


def test_replacement_preserves_other_declared_facts() -> None:
    original = classification()
    changed = replace(original, rotation_class=RetailProductRotationClass.C)
    assert changed.product_identity is original.product_identity
    assert changed.classification_scheme_id == original.classification_scheme_id
    assert changed.classification_scheme_version == original.classification_scheme_version
    assert changed.rotation_class is RetailProductRotationClass.C


def test_contract_has_no_classifier_or_commercial_fields() -> None:
    module = __import__(
        "sp001.contracts.retail_product_rotation_classification", fromlist=["*"]
    )
    functions = tuple(
        name
        for name, value in vars(module).items()
        if inspect.isfunction(value) and value.__module__ == module.__name__
    )
    assert functions == ()
    names = {field.name for field in fields(RetailProductDeclaredRotationClassification)}
    assert names.isdisjoint({"units_sold", "sales_threshold", "margin", "priority"})


def test_contract_adds_no_calculation_inventory_recommendation_or_io() -> None:
    module = __import__(
        "sp001.contracts.retail_product_rotation_classification", fromlist=["*"]
    )
    source = inspect.getsource(module).casefold()
    for forbidden in (
        "units_sold", "sell_through", "threshold", "inventory", "stock",
        "substitute", "margin", "recommend", "priority", "requests", "open(",
    ):
        assert forbidden not in source
