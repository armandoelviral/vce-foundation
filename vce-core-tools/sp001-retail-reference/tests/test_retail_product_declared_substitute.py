from dataclasses import FrozenInstanceError, fields, replace
import inspect

import pytest

from sp001.contracts.retail_product_declared_substitute import (
    RetailProductDeclaredSubstitute,
)
from sp001.contracts.retail_product_identity import (
    RetailProductIdentity,
)


def create_product_identity(
    *,
    product_id: str,
    sku: str,
) -> RetailProductIdentity:
    return RetailProductIdentity(
        product_id=product_id,
        sku=sku,
        catalog_id="catalog-001",
        catalog_version=1,
    )


def create_declaration() -> RetailProductDeclaredSubstitute:
    return RetailProductDeclaredSubstitute(
        product_identity=create_product_identity(
            product_id="product-001",
            sku="SKU-001",
        ),
        substitute_product_identity=create_product_identity(
            product_id="product-099",
            sku="SKU-099",
        ),
        substitution_scheme_id="substitution-scheme-001",
        substitution_scheme_version=1,
    )


def test_declared_substitute_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(RetailProductDeclaredSubstitute)
    ) == (
        "product_identity",
        "substitute_product_identity",
        "substitution_scheme_id",
        "substitution_scheme_version",
    )


def test_declared_substitute_is_immutable() -> None:
    declaration = create_declaration()

    with pytest.raises(FrozenInstanceError):
        declaration.substitution_scheme_version = 2  # type: ignore[misc]


def test_declared_substitute_uses_slots() -> None:
    assert not hasattr(create_declaration(), "__dict__")


def test_declaration_preserves_exact_product_references() -> None:
    product = create_product_identity(
        product_id="product-001",
        sku="SKU-001",
    )
    substitute = create_product_identity(
        product_id="product-099",
        sku="SKU-099",
    )
    declaration = RetailProductDeclaredSubstitute(
        product_identity=product,
        substitute_product_identity=substitute,
        substitution_scheme_id="scheme-001",
        substitution_scheme_version=1,
    )

    assert declaration.product_identity is product
    assert declaration.substitute_product_identity is substitute


def test_declaration_preserves_scheme_identity_and_version() -> None:
    declaration = create_declaration()

    assert declaration.substitution_scheme_id == (
        "substitution-scheme-001"
    )
    assert declaration.substitution_scheme_version == 1


def test_equal_declarations_are_deterministically_equal() -> None:
    assert create_declaration() == create_declaration()


def test_substitution_direction_does_not_imply_reciprocity() -> None:
    declaration = create_declaration()
    reverse = RetailProductDeclaredSubstitute(
        product_identity=declaration.substitute_product_identity,
        substitute_product_identity=declaration.product_identity,
        substitution_scheme_id=declaration.substitution_scheme_id,
        substitution_scheme_version=(
            declaration.substitution_scheme_version
        ),
    )

    assert reverse != declaration
    assert reverse.product_identity is (
        declaration.substitute_product_identity
    )


def test_distinct_scheme_versions_remain_distinct() -> None:
    declaration = create_declaration()

    assert replace(
        declaration,
        substitution_scheme_version=2,
    ) != declaration


@pytest.mark.parametrize(
    "field_name",
    ["product_identity", "substitute_product_identity"],
)
def test_product_members_require_exact_identity_type(
    field_name: str,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "product_identity must be a RetailProductIdentity"
            if field_name == "product_identity"
            else (
                "substitute_product_identity must be a "
                "RetailProductIdentity"
            )
        ),
    ):
        replace(
            create_declaration(),
            **{field_name: object()},
        )


@pytest.mark.parametrize(
    "value",
    ["", " ", "\t", None, 1],
)
def test_substitution_scheme_id_requires_nonempty_string(
    value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="substitution_scheme_id must not be empty",
    ):
        replace(
            create_declaration(),
            substitution_scheme_id=value,
        )


@pytest.mark.parametrize(
    "value",
    [True, False, 0, -1, 1.0, "1", None],
)
def test_substitution_scheme_version_requires_positive_integer(
    value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "substitution_scheme_version must be a "
            "positive integer"
        ),
    ):
        replace(
            create_declaration(),
            substitution_scheme_version=value,
        )


@pytest.mark.parametrize("value", [1, 2, 100])
def test_positive_substitution_scheme_version_is_accepted(
    value: int,
) -> None:
    declaration = replace(
        create_declaration(),
        substitution_scheme_version=value,
    )

    assert declaration.substitution_scheme_version == value


def test_exact_self_substitution_is_rejected() -> None:
    product = create_product_identity(
        product_id="product-001",
        sku="SKU-001",
    )

    with pytest.raises(
        ValueError,
        match="a product cannot substitute itself",
    ):
        RetailProductDeclaredSubstitute(
            product_identity=product,
            substitute_product_identity=product,
            substitution_scheme_id="scheme-001",
            substitution_scheme_version=1,
        )


def test_equal_reconstructed_self_substitution_is_rejected() -> None:
    product = create_product_identity(
        product_id="product-001",
        sku="SKU-001",
    )
    reconstructed = replace(product)

    assert reconstructed == product
    assert reconstructed is not product

    with pytest.raises(
        ValueError,
        match="a product cannot substitute itself",
    ):
        RetailProductDeclaredSubstitute(
            product_identity=product,
            substitute_product_identity=reconstructed,
            substitution_scheme_id="scheme-001",
            substitution_scheme_version=1,
        )


def test_declaration_has_no_ranking_or_recommendation_fields() -> None:
    field_names = {
        field.name
        for field in fields(RetailProductDeclaredSubstitute)
    }

    assert field_names.isdisjoint(
        {
            "rank",
            "priority",
            "score",
            "preferred",
            "recommendation",
            "reason",
        }
    )


def test_declaration_has_no_inventory_or_commercial_fields() -> None:
    field_names = {
        field.name
        for field in fields(RetailProductDeclaredSubstitute)
    }

    assert field_names.isdisjoint(
        {
            "observed_quantity",
            "availability",
            "stock_status",
            "margin",
            "sell_through",
            "context_scope",
            "snapshot_id",
        }
    )


def test_contract_introduces_no_graph_lookup_or_io_capability() -> None:
    module = __import__(
        "sp001.contracts.retail_product_declared_substitute",
        fromlist=["*"],
    )
    source = inspect.getsource(module).lower()

    forbidden = (
        "graph",
        "lookup",
        "select",
        "recommend",
        "requests",
        "notion",
        "openai",
        "subprocess",
        "pathlib",
    )

    assert all(term not in source for term in forbidden)
