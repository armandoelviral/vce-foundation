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
from sp001.contracts.retail_product_derived_margin_amount import (
    RetailProductDerivedMarginAmount,
)
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
DERIVED_AT = datetime(2026, 9, 10, 13, 0, tzinfo=UTC)


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


def create_basis() -> RetailProductMarginCalculationBasis:
    product_identity = create_product_identity()
    context_scope = create_context_scope()
    currency_identity = create_currency_identity()
    price = RetailProductObservedPrice(
        product_identity=product_identity,
        context_scope=context_scope,
        monetary_amount=create_amount(
            currency_identity=currency_identity,
            minor_unit_amount=15000,
        ),
        pricing_scheme_id="observed-store-price",
        pricing_scheme_version=1,
        provenance_binding=create_binding(
            context_scope=context_scope,
            kind="price",
            observed_at=PRICE_OBSERVED_AT,
        ),
    )
    cost = RetailProductObservedCost(
        product_identity=product_identity,
        context_scope=context_scope,
        monetary_amount=create_amount(
            currency_identity=currency_identity,
            minor_unit_amount=9000,
        ),
        costing_scheme_id="observed-product-cost",
        costing_scheme_version=1,
        provenance_binding=create_binding(
            context_scope=context_scope,
            kind="cost",
            observed_at=COST_OBSERVED_AT,
        ),
    )
    return RetailProductMarginCalculationBasis(
        price_observation=price,
        cost_observation=cost,
        calculation_scheme_id="declared-margin-method",
        calculation_scheme_version=1,
    )


def create_result(
    *,
    minor_unit_amount: int = 6000,
    derived_at: datetime = DERIVED_AT,
) -> RetailProductDerivedMarginAmount:
    basis = create_basis()
    currency_identity = (
        basis.price_observation
        .monetary_amount
        .currency_identity
    )
    return RetailProductDerivedMarginAmount(
        result_id="margin-amount-result-001",
        result_version=1,
        calculation_basis=basis,
        margin_amount=create_amount(
            currency_identity=currency_identity,
            minor_unit_amount=minor_unit_amount,
        ),
        derived_at=derived_at,
    )


def test_derived_margin_amount_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(RetailProductDerivedMarginAmount)
    ) == (
        "result_id",
        "result_version",
        "calculation_basis",
        "margin_amount",
        "derived_at",
    )


def test_derived_margin_amount_is_immutable() -> None:
    result = create_result()

    with pytest.raises(FrozenInstanceError):
        result.result_version = 2  # type: ignore[misc]


def test_derived_margin_amount_uses_slots() -> None:
    assert not hasattr(create_result(), "__dict__")


def test_exact_basis_and_amount_references_are_preserved() -> None:
    basis = create_basis()
    currency_identity = (
        basis.price_observation
        .monetary_amount
        .currency_identity
    )
    amount = create_amount(
        currency_identity=currency_identity,
        minor_unit_amount=6000,
    )
    result = RetailProductDerivedMarginAmount(
        result_id="margin-amount-result-001",
        result_version=1,
        calculation_basis=basis,
        margin_amount=amount,
        derived_at=DERIVED_AT,
    )

    assert result.calculation_basis is basis
    assert result.margin_amount is amount


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_result_id_requires_string(value: object) -> None:
    with pytest.raises(
        TypeError,
        match="result_id must be a string",
    ):
        replace(
            create_result(),
            result_id=value,  # type: ignore[arg-type]
        )


def test_empty_result_id_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="result_id must not be empty",
    ):
        replace(create_result(), result_id="")


@pytest.mark.parametrize("value", [" ", "\t", " result id "])
def test_result_id_is_preserved_literally(value: str) -> None:
    result = replace(create_result(), result_id=value)

    assert result.result_id == value


@pytest.mark.parametrize("value", [True, False, 1.0, "1", None])
def test_result_version_requires_strict_integer(
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="result_version must be an integer",
    ):
        replace(
            create_result(),
            result_version=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", [0, -1, -(10**30)])
def test_result_version_requires_positive_value(value: int) -> None:
    with pytest.raises(
        ValueError,
        match="result_version must be positive",
    ):
        replace(create_result(), result_version=value)


def test_calculation_basis_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "calculation_basis must be a "
            "RetailProductMarginCalculationBasis"
        ),
    ):
        replace(
            create_result(),
            calculation_basis=object(),  # type: ignore[arg-type]
        )


def test_margin_amount_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "margin_amount must be a "
            "RetailCommercialMonetaryAmount"
        ),
    ):
        replace(
            create_result(),
            margin_amount=object(),  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "minor_unit_amount",
    [-(10**30), -6000, -1, 0, 1, 6000, 10**30],
)
def test_signed_margin_amounts_are_preserved_exactly(
    minor_unit_amount: int,
) -> None:
    result = create_result(
        minor_unit_amount=minor_unit_amount,
    )

    assert result.margin_amount.minor_unit_amount == minor_unit_amount


def test_reconstructed_equal_currency_identity_is_accepted() -> None:
    result = create_result()
    reconstructed_currency = replace(
        result.margin_amount.currency_identity
    )

    assert reconstructed_currency == (
        result.calculation_basis
        .price_observation
        .monetary_amount
        .currency_identity
    )
    assert reconstructed_currency is not (
        result.calculation_basis
        .price_observation
        .monetary_amount
        .currency_identity
    )

    reconstructed_amount = replace(
        result.margin_amount,
        currency_identity=reconstructed_currency,
    )
    reconstructed_result = replace(
        result,
        margin_amount=reconstructed_amount,
    )

    assert reconstructed_result.margin_amount is reconstructed_amount


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("currency_code", "USD"),
        ("currency_scheme_id", "PRIVATE-CURRENCY-SCHEME"),
        ("currency_scheme_version", 2),
    ],
)
def test_mismatched_margin_currency_identity_is_rejected(
    field_name: str,
    value: object,
) -> None:
    result = create_result()
    foreign_currency = replace(
        result.margin_amount.currency_identity,
        **{field_name: value},
    )
    foreign_amount = replace(
        result.margin_amount,
        currency_identity=foreign_currency,
    )

    with pytest.raises(
        ValueError,
        match=(
            "margin_amount currency_identity must match "
            "calculation basis currency_identity"
        ),
    ):
        replace(result, margin_amount=foreign_amount)


@pytest.mark.parametrize(
    "derived_at",
    [None, "2026-09-10T13:00:00Z", 0, object()],
)
def test_derived_at_requires_datetime(derived_at: object) -> None:
    with pytest.raises(
        TypeError,
        match="derived_at must be a datetime",
    ):
        replace(
            create_result(),
            derived_at=derived_at,  # type: ignore[arg-type]
        )


def test_derived_at_requires_timezone_awareness() -> None:
    with pytest.raises(
        ValueError,
        match="derived_at must be timezone-aware",
    ):
        create_result(
            derived_at=datetime(2026, 9, 10, 13, 0),
        )


def test_derived_at_is_preserved_exactly() -> None:
    result = create_result()

    assert result.derived_at is DERIVED_AT


def test_result_contains_no_ratio_or_indeterminate_fields() -> None:
    field_names = {
        field.name
        for field in fields(RetailProductDerivedMarginAmount)
    }

    assert field_names.isdisjoint(
        {
            "margin_ratio",
            "margin_percentage",
            "markup",
            "numerator",
            "denominator",
            "status",
            "reason",
        }
    )


def test_contract_does_not_calculate_or_restrict_margin_sign() -> None:
    module = inspect.getmodule(RetailProductDerivedMarginAmount)
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
    assert "minor_unit_amount" not in attribute_names


def test_contract_imports_no_external_or_execution_capability() -> None:
    module = inspect.getmodule(RetailProductDerivedMarginAmount)
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


def test_contract_defines_no_formula_or_decision_function() -> None:
    module = inspect.getmodule(RetailProductDerivedMarginAmount)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    function_names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert function_names == {"__post_init__"}
