from dataclasses import FrozenInstanceError, fields, replace
from datetime import UTC, datetime
import ast
import inspect

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.retail_commercial_currency_identity import (
    RetailCommercialCurrencyIdentity,
)
from sp001.contracts.retail_commercial_monetary_amount import (
    RetailCommercialMonetaryAmount,
)
from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)
from sp001.contracts.retail_context_observation_provenance import (
    RetailContextObservationProvenance,
)
from sp001.contracts.retail_context_observation_provenance_binding import (
    RetailContextObservationProvenanceBinding,
)
from sp001.contracts.retail_context_scope import RetailContextScope
from sp001.contracts.retail_context_snapshot import RetailContextSnapshot
from sp001.contracts.retail_product_identity import RetailProductIdentity
from sp001.contracts.retail_product_observed_price import (
    RetailProductObservedPrice,
)


OBSERVED_AT = datetime(2026, 9, 10, 12, 0, tzinfo=UTC)


def create_product_identity() -> RetailProductIdentity:
    return RetailProductIdentity(
        product_id="product-001",
        sku="SKU-001",
        catalog_id="catalog-001",
        catalog_version=1,
    )


def create_context_scope() -> RetailContextScope:
    return RetailContextScope(
        context_id="context-001",
        commercial_channel_id="store",
        point_of_sale_id="store-001",
        department_id="childrens-apparel",
        profile_version=1,
    )


def create_currency_identity() -> RetailCommercialCurrencyIdentity:
    return RetailCommercialCurrencyIdentity(
        currency_code="MXN",
        currency_scheme_id="ISO-4217",
        currency_scheme_version=1,
    )


def create_amount(
    *,
    minor_unit_amount: int = 12500,
) -> RetailCommercialMonetaryAmount:
    return RetailCommercialMonetaryAmount(
        currency_identity=create_currency_identity(),
        minor_unit_amount=minor_unit_amount,
    )


def create_binding(
    *,
    context_scope: RetailContextScope,
) -> RetailContextObservationProvenanceBinding:
    dimension = RetailContextDimension(
        dimension_id="price-observation-001",
        dimension_type="PRODUCT_PRICE",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.MEASURED,
        value="12500 MXN minor units",
    )
    snapshot = RetailContextSnapshot(
        snapshot_id="snapshot-price-001",
        snapshot_version=1,
        case_id="case-001",
        dimensions=(dimension,),
        context_scope=context_scope,
    )
    source_identity = KnowledgeSourceIdentity(
        source_id="price-source-001",
        source_version="1",
        source_content_digest=KnowledgeContentDigest(
            algorithm="SHA-256",
            value="0" * 64,
        ),
    )
    provenance = RetailContextObservationProvenance(
        observation_id="price-observation-001",
        observation_version=1,
        case_id="case-001",
        snapshot_id="snapshot-price-001",
        snapshot_version=1,
        dimension_id="price-observation-001",
        source_identity=source_identity,
        observed_at=OBSERVED_AT,
        recorded_at=OBSERVED_AT,
        effective_from=OBSERVED_AT,
        evidence_ids=("price-evidence-001",),
    )
    return RetailContextObservationProvenanceBinding(
        snapshot=snapshot,
        dimension=dimension,
        provenance=provenance,
    )


def create_observed_price(
    *,
    minor_unit_amount: int = 12500,
) -> RetailProductObservedPrice:
    context_scope = create_context_scope()
    return RetailProductObservedPrice(
        product_identity=create_product_identity(),
        context_scope=context_scope,
        monetary_amount=create_amount(
            minor_unit_amount=minor_unit_amount,
        ),
        pricing_scheme_id="observed-store-price",
        pricing_scheme_version=1,
        provenance_binding=create_binding(
            context_scope=context_scope,
        ),
    )


def test_observed_price_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(RetailProductObservedPrice)
    ) == (
        "product_identity",
        "context_scope",
        "monetary_amount",
        "pricing_scheme_id",
        "pricing_scheme_version",
        "provenance_binding",
    )


def test_observed_price_is_immutable() -> None:
    observation = create_observed_price()

    with pytest.raises(FrozenInstanceError):
        observation.pricing_scheme_version = 2  # type: ignore[misc]


def test_observed_price_uses_slots() -> None:
    assert not hasattr(create_observed_price(), "__dict__")


def test_exact_typed_references_are_preserved() -> None:
    product = create_product_identity()
    scope = create_context_scope()
    amount = create_amount()
    binding = create_binding(context_scope=scope)

    observation = RetailProductObservedPrice(
        product_identity=product,
        context_scope=scope,
        monetary_amount=amount,
        pricing_scheme_id="observed-store-price",
        pricing_scheme_version=1,
        provenance_binding=binding,
    )

    assert observation.product_identity is product
    assert observation.context_scope is scope
    assert observation.monetary_amount is amount
    assert observation.provenance_binding is binding


@pytest.mark.parametrize(
    ("field_name", "message"),
    [
        (
            "product_identity",
            "product_identity must be a RetailProductIdentity",
        ),
        (
            "context_scope",
            "context_scope must be a RetailContextScope",
        ),
        (
            "monetary_amount",
            "monetary_amount must be a RetailCommercialMonetaryAmount",
        ),
        (
            "provenance_binding",
            "provenance_binding must be a RetailContextObservationProvenanceBinding",
        ),
    ],
)
def test_typed_members_require_exact_types(
    field_name: str,
    message: str,
) -> None:
    with pytest.raises(TypeError, match=message):
        replace(
            create_observed_price(),
            **{field_name: object()},
        )


@pytest.mark.parametrize("minor_unit_amount", [0, 1, 12500, 10**30])
def test_nonnegative_price_amounts_are_accepted_exactly(
    minor_unit_amount: int,
) -> None:
    observation = create_observed_price(
        minor_unit_amount=minor_unit_amount,
    )

    assert (
        observation.monetary_amount.minor_unit_amount
        == minor_unit_amount
    )


@pytest.mark.parametrize("minor_unit_amount", [-1, -12500, -(10**30)])
def test_negative_price_amounts_are_rejected(
    minor_unit_amount: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="monetary_amount must not be negative",
    ):
        create_observed_price(
            minor_unit_amount=minor_unit_amount,
        )


def test_generic_signed_amount_remains_valid_outside_price() -> None:
    amount = create_amount(minor_unit_amount=-1)

    assert amount.minor_unit_amount == -1

    with pytest.raises(
        ValueError,
        match="monetary_amount must not be negative",
    ):
        replace(
            create_observed_price(),
            monetary_amount=amount,
        )


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_pricing_scheme_id_requires_string(value: object) -> None:
    with pytest.raises(
        TypeError,
        match="pricing_scheme_id must be a string",
    ):
        replace(
            create_observed_price(),
            pricing_scheme_id=value,  # type: ignore[arg-type]
        )


def test_empty_pricing_scheme_id_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="pricing_scheme_id must not be empty",
    ):
        replace(
            create_observed_price(),
            pricing_scheme_id="",
        )


@pytest.mark.parametrize("value", [" ", "\t", " price scheme "])
def test_pricing_scheme_id_is_preserved_without_normalization(
    value: str,
) -> None:
    observation = replace(
        create_observed_price(),
        pricing_scheme_id=value,
    )

    assert observation.pricing_scheme_id == value


@pytest.mark.parametrize("value", [True, False, 1.0, "1", None])
def test_pricing_scheme_version_requires_strict_integer(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="pricing_scheme_version must be an integer",
    ):
        replace(
            create_observed_price(),
            pricing_scheme_version=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", [0, -1, -(10**30)])
def test_pricing_scheme_version_requires_positive_value(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="pricing_scheme_version must be positive",
    ):
        replace(
            create_observed_price(),
            pricing_scheme_version=value,
        )


def test_reconstructed_equal_context_scope_is_accepted() -> None:
    snapshot_scope = create_context_scope()
    reconstructed_scope = replace(snapshot_scope)

    assert reconstructed_scope == snapshot_scope
    assert reconstructed_scope is not snapshot_scope

    observation = RetailProductObservedPrice(
        product_identity=create_product_identity(),
        context_scope=reconstructed_scope,
        monetary_amount=create_amount(),
        pricing_scheme_id="observed-store-price",
        pricing_scheme_version=1,
        provenance_binding=create_binding(
            context_scope=snapshot_scope,
        ),
    )

    assert observation.context_scope == (
        observation.provenance_binding.snapshot.context_scope
    )


def test_different_snapshot_context_scope_is_rejected() -> None:
    observation = create_observed_price()
    different_scope = replace(
        observation.context_scope,
        point_of_sale_id="store-002",
    )

    with pytest.raises(
        ValueError,
        match=(
            "context_scope must match the context scope "
            "referenced by provenance_binding snapshot"
        ),
    ):
        replace(
            observation,
            context_scope=different_scope,
        )


def test_snapshot_and_temporal_identity_are_not_duplicated() -> None:
    field_names = {
        field.name
        for field in fields(RetailProductObservedPrice)
    }

    assert field_names.isdisjoint(
        {
            "snapshot_id",
            "snapshot_version",
            "case_id",
            "dimension_id",
            "observation_id",
            "observation_version",
            "observed_at",
            "recorded_at",
            "effective_from",
            "effective_until",
            "evidence_ids",
        }
    )


def test_price_observation_has_no_aggregation_period() -> None:
    observation = create_observed_price()

    assert not hasattr(observation, "observation_period")
    assert not hasattr(observation, "period_from")
    assert not hasattr(observation, "period_until")
    assert (
        observation.provenance_binding.provenance.observed_at
        == OBSERVED_AT
    )


def test_zero_price_remains_an_uninterpreted_observation() -> None:
    observation = create_observed_price(minor_unit_amount=0)

    assert observation.monetary_amount.minor_unit_amount == 0
    assert not hasattr(observation, "price_status")
    assert not hasattr(observation, "availability")
    assert not hasattr(observation, "commercial_decision")


def test_contract_adds_no_price_basis_or_margin_fields() -> None:
    field_names = {
        field.name
        for field in fields(RetailProductObservedPrice)
    }

    assert field_names.isdisjoint(
        {
            "list_price",
            "sale_price",
            "promotion_price",
            "transaction_price",
            "tax",
            "discount",
            "cost",
            "revenue",
            "margin",
        }
    )


def test_contract_imports_no_external_or_execution_capability() -> None:
    module = inspect.getmodule(RetailProductObservedPrice)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    imported_roots = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_roots.update(
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.module is not None
    )

    assert imported_roots.isdisjoint(
        {
            "os",
            "pathlib",
            "subprocess",
            "sqlite3",
            "requests",
            "httpx",
            "urllib",
            "openai",
            "notion_client",
        }
    )


def test_contract_defines_no_calculation_or_decision_function() -> None:
    module = inspect.getmodule(RetailProductObservedPrice)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    function_names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert function_names == {"__post_init__"}
