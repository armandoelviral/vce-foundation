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
from sp001.contracts.retail_product_margin_calculation_basis import (
    RetailProductMarginCalculationBasis,
)
from sp001.contracts.retail_product_observed_cost import (
    RetailProductObservedCost,
)
from sp001.contracts.retail_product_observed_price import (
    RetailProductObservedPrice,
)


PRICE_OBSERVED_AT = datetime(2026, 9, 10, 12, 0, tzinfo=UTC)
COST_OBSERVED_AT = datetime(2026, 9, 9, 12, 0, tzinfo=UTC)


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
    currency_identity: RetailCommercialCurrencyIdentity,
    minor_unit_amount: int,
) -> RetailCommercialMonetaryAmount:
    return RetailCommercialMonetaryAmount(
        currency_identity=currency_identity,
        minor_unit_amount=minor_unit_amount,
    )


def create_binding(
    *,
    context_scope: RetailContextScope,
    kind: str,
    observed_at: datetime,
) -> RetailContextObservationProvenanceBinding:
    dimension_id = f"{kind}-observation-001"
    snapshot_id = f"snapshot-{kind}-001"
    dimension = RetailContextDimension(
        dimension_id=dimension_id,
        dimension_type=f"PRODUCT_{kind.upper()}",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.MEASURED,
        value=f"{kind} monetary observation",
    )
    snapshot = RetailContextSnapshot(
        snapshot_id=snapshot_id,
        snapshot_version=1,
        case_id="case-001",
        dimensions=(dimension,),
        context_scope=context_scope,
    )
    source_identity = KnowledgeSourceIdentity(
        source_id=f"{kind}-source-001",
        source_version="1",
        source_content_digest=KnowledgeContentDigest(
            algorithm="SHA-256",
            value=("0" if kind == "price" else "1") * 64,
        ),
    )
    provenance = RetailContextObservationProvenance(
        observation_id=f"{kind}-observation-001",
        observation_version=1,
        case_id="case-001",
        snapshot_id=snapshot_id,
        snapshot_version=1,
        dimension_id=dimension_id,
        source_identity=source_identity,
        observed_at=observed_at,
        recorded_at=observed_at,
        effective_from=observed_at,
        evidence_ids=(f"{kind}-evidence-001",),
    )
    return RetailContextObservationProvenanceBinding(
        snapshot=snapshot,
        dimension=dimension,
        provenance=provenance,
    )


def create_price_observation(
    *,
    product_identity: RetailProductIdentity,
    context_scope: RetailContextScope,
    currency_identity: RetailCommercialCurrencyIdentity,
    minor_unit_amount: int = 15000,
    observed_at: datetime = PRICE_OBSERVED_AT,
) -> RetailProductObservedPrice:
    return RetailProductObservedPrice(
        product_identity=product_identity,
        context_scope=context_scope,
        monetary_amount=create_amount(
            currency_identity=currency_identity,
            minor_unit_amount=minor_unit_amount,
        ),
        pricing_scheme_id="observed-store-price",
        pricing_scheme_version=1,
        provenance_binding=create_binding(
            context_scope=context_scope,
            kind="price",
            observed_at=observed_at,
        ),
    )


def create_cost_observation(
    *,
    product_identity: RetailProductIdentity,
    context_scope: RetailContextScope,
    currency_identity: RetailCommercialCurrencyIdentity,
    minor_unit_amount: int = 9000,
    observed_at: datetime = COST_OBSERVED_AT,
) -> RetailProductObservedCost:
    return RetailProductObservedCost(
        product_identity=product_identity,
        context_scope=context_scope,
        monetary_amount=create_amount(
            currency_identity=currency_identity,
            minor_unit_amount=minor_unit_amount,
        ),
        costing_scheme_id="observed-product-cost",
        costing_scheme_version=1,
        provenance_binding=create_binding(
            context_scope=context_scope,
            kind="cost",
            observed_at=observed_at,
        ),
    )


def create_basis(
    *,
    price_amount: int = 15000,
    cost_amount: int = 9000,
) -> RetailProductMarginCalculationBasis:
    product_identity = create_product_identity()
    context_scope = create_context_scope()
    currency_identity = create_currency_identity()
    return RetailProductMarginCalculationBasis(
        price_observation=create_price_observation(
            product_identity=product_identity,
            context_scope=context_scope,
            currency_identity=currency_identity,
            minor_unit_amount=price_amount,
        ),
        cost_observation=create_cost_observation(
            product_identity=product_identity,
            context_scope=context_scope,
            currency_identity=currency_identity,
            minor_unit_amount=cost_amount,
        ),
        calculation_scheme_id="declared-margin-method",
        calculation_scheme_version=1,
    )


def test_margin_calculation_basis_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(RetailProductMarginCalculationBasis)
    ) == (
        "price_observation",
        "cost_observation",
        "calculation_scheme_id",
        "calculation_scheme_version",
    )


def test_margin_calculation_basis_is_immutable() -> None:
    basis = create_basis()

    with pytest.raises(FrozenInstanceError):
        basis.calculation_scheme_version = 2  # type: ignore[misc]


def test_margin_calculation_basis_uses_slots() -> None:
    assert not hasattr(create_basis(), "__dict__")


def test_complete_source_observations_are_preserved() -> None:
    basis = create_basis()

    assert isinstance(
        basis.price_observation,
        RetailProductObservedPrice,
    )
    assert isinstance(
        basis.cost_observation,
        RetailProductObservedCost,
    )
    assert basis.price_observation.provenance_binding is not None
    assert basis.cost_observation.provenance_binding is not None


@pytest.mark.parametrize(
    ("field_name", "message"),
    [
        (
            "price_observation",
            "price_observation must be a RetailProductObservedPrice",
        ),
        (
            "cost_observation",
            "cost_observation must be a RetailProductObservedCost",
        ),
    ],
)
def test_observations_require_exact_types(
    field_name: str,
    message: str,
) -> None:
    with pytest.raises(TypeError, match=message):
        replace(
            create_basis(),
            **{field_name: object()},
        )


def test_reconstructed_equal_inputs_are_accepted() -> None:
    price_product = create_product_identity()
    cost_product = replace(price_product)
    price_scope = create_context_scope()
    cost_scope = replace(price_scope)
    price_currency = create_currency_identity()
    cost_currency = replace(price_currency)

    assert price_product == cost_product
    assert price_product is not cost_product
    assert price_scope == cost_scope
    assert price_scope is not cost_scope
    assert price_currency == cost_currency
    assert price_currency is not cost_currency

    basis = RetailProductMarginCalculationBasis(
        price_observation=create_price_observation(
            product_identity=price_product,
            context_scope=price_scope,
            currency_identity=price_currency,
        ),
        cost_observation=create_cost_observation(
            product_identity=cost_product,
            context_scope=cost_scope,
            currency_identity=cost_currency,
        ),
        calculation_scheme_id="declared-margin-method",
        calculation_scheme_version=1,
    )

    assert (
        basis.price_observation.product_identity
        == basis.cost_observation.product_identity
    )


def test_mismatched_product_identity_is_rejected() -> None:
    basis = create_basis()
    foreign_product = replace(
        basis.cost_observation.product_identity,
        product_id="product-002",
    )

    with pytest.raises(
        ValueError,
        match=(
            "cost observation product_identity must match "
            "price observation product_identity"
        ),
    ):
        replace(
            basis,
            cost_observation=replace(
                basis.cost_observation,
                product_identity=foreign_product,
            ),
        )


def test_mismatched_context_scope_is_rejected() -> None:
    basis = create_basis()
    foreign_scope = replace(
        basis.cost_observation.context_scope,
        point_of_sale_id="store-002",
    )
    foreign_binding = create_binding(
        context_scope=foreign_scope,
        kind="cost",
        observed_at=COST_OBSERVED_AT,
    )

    with pytest.raises(
        ValueError,
        match=(
            "cost observation context_scope must match "
            "price observation context_scope"
        ),
    ):
        replace(
            basis,
            cost_observation=replace(
                basis.cost_observation,
                context_scope=foreign_scope,
                provenance_binding=foreign_binding,
            ),
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("currency_code", "USD"),
        ("currency_scheme_id", "PRIVATE-CURRENCY-SCHEME"),
        ("currency_scheme_version", 2),
    ],
)
def test_mismatched_currency_identity_is_rejected(
    field_name: str,
    value: object,
) -> None:
    basis = create_basis()
    cost_currency = (
        basis.cost_observation.monetary_amount.currency_identity
    )
    foreign_currency = replace(
        cost_currency,
        **{field_name: value},
    )
    foreign_amount = replace(
        basis.cost_observation.monetary_amount,
        currency_identity=foreign_currency,
    )

    with pytest.raises(
        ValueError,
        match=(
            "cost observation currency_identity must match "
            "price observation currency_identity"
        ),
    ):
        replace(
            basis,
            cost_observation=replace(
                basis.cost_observation,
                monetary_amount=foreign_amount,
            ),
        )


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_calculation_scheme_id_requires_string(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="calculation_scheme_id must be a string",
    ):
        replace(
            create_basis(),
            calculation_scheme_id=value,  # type: ignore[arg-type]
        )


def test_empty_calculation_scheme_id_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="calculation_scheme_id must not be empty",
    ):
        replace(
            create_basis(),
            calculation_scheme_id="",
        )


@pytest.mark.parametrize("value", [" ", "\t", " margin method "])
def test_calculation_scheme_id_is_preserved_literally(
    value: str,
) -> None:
    basis = replace(
        create_basis(),
        calculation_scheme_id=value,
    )

    assert basis.calculation_scheme_id == value


@pytest.mark.parametrize("value", [True, False, 1.0, "1", None])
def test_calculation_scheme_version_requires_strict_integer(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="calculation_scheme_version must be an integer",
    ):
        replace(
            create_basis(),
            calculation_scheme_version=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", [0, -1, -(10**30)])
def test_calculation_scheme_version_requires_positive_value(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="calculation_scheme_version must be positive",
    ):
        replace(
            create_basis(),
            calculation_scheme_version=value,
        )


@pytest.mark.parametrize(
    ("price_amount", "cost_amount"),
    [(0, 0), (0, 9000), (15000, 0)],
)
def test_zero_monetary_inputs_remain_admissible(
    price_amount: int,
    cost_amount: int,
) -> None:
    basis = create_basis(
        price_amount=price_amount,
        cost_amount=cost_amount,
    )

    assert (
        basis.price_observation.monetary_amount.minor_unit_amount
        == price_amount
    )
    assert (
        basis.cost_observation.monetary_amount.minor_unit_amount
        == cost_amount
    )


def test_distinct_observation_instants_are_accepted() -> None:
    basis = create_basis()
    price_instant = (
        basis.price_observation
        .provenance_binding
        .provenance
        .observed_at
    )
    cost_instant = (
        basis.cost_observation
        .provenance_binding
        .provenance
        .observed_at
    )

    assert price_instant == PRICE_OBSERVED_AT
    assert cost_instant == COST_OBSERVED_AT
    assert price_instant != cost_instant


def test_observation_and_snapshot_identity_are_not_duplicated() -> None:
    field_names = {
        field.name
        for field in fields(RetailProductMarginCalculationBasis)
    }

    assert field_names.isdisjoint(
        {
            "product_identity",
            "context_scope",
            "currency_identity",
            "price_observation_id",
            "cost_observation_id",
            "snapshot_id",
            "snapshot_version",
            "observed_at",
            "effective_from",
            "effective_until",
        }
    )


def test_basis_contains_no_margin_result_or_formula_fields() -> None:
    field_names = {
        field.name
        for field in fields(RetailProductMarginCalculationBasis)
    }

    assert field_names.isdisjoint(
        {
            "gross_margin",
            "margin_amount",
            "margin_ratio",
            "margin_percentage",
            "markup",
            "numerator",
            "denominator",
            "derived_at",
        }
    )


def test_contract_performs_no_arithmetic_or_temporal_alignment() -> None:
    module = inspect.getmodule(RetailProductMarginCalculationBasis)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))

    assert not any(
        isinstance(node, ast.BinOp)
        for node in ast.walk(tree)
    )

    attribute_names = {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
    }
    assert attribute_names.isdisjoint(
        {
            "minor_unit_amount",
            "observed_at",
            "effective_from",
            "effective_until",
        }
    )


def test_contract_imports_no_external_or_execution_capability() -> None:
    module = inspect.getmodule(RetailProductMarginCalculationBasis)
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
    module = inspect.getmodule(RetailProductMarginCalculationBasis)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    function_names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert function_names == {"__post_init__"}
