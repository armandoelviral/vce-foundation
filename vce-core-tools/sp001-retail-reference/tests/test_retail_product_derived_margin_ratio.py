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
from sp001.contracts.retail_product_derived_margin_ratio import (
    RetailProductDerivedMarginRatio,
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
    numerator: int = 2,
    denominator: int = 5,
    derived_at: datetime = DERIVED_AT,
) -> RetailProductDerivedMarginRatio:
    return RetailProductDerivedMarginRatio(
        result_id="margin-ratio-result-001",
        result_version=1,
        calculation_basis=create_basis(),
        numerator=numerator,
        denominator=denominator,
        derived_at=derived_at,
    )


def test_derived_margin_ratio_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(RetailProductDerivedMarginRatio)
    ) == (
        "result_id",
        "result_version",
        "calculation_basis",
        "numerator",
        "denominator",
        "derived_at",
    )


def test_derived_margin_ratio_is_immutable() -> None:
    result = create_result()

    with pytest.raises(FrozenInstanceError):
        result.numerator = 1  # type: ignore[misc]


def test_derived_margin_ratio_uses_slots() -> None:
    assert not hasattr(create_result(), "__dict__")


def test_exact_calculation_basis_reference_is_preserved() -> None:
    basis = create_basis()
    result = RetailProductDerivedMarginRatio(
        result_id="margin-ratio-result-001",
        result_version=1,
        calculation_basis=basis,
        numerator=2,
        denominator=5,
        derived_at=DERIVED_AT,
    )

    assert result.calculation_basis is basis


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


@pytest.mark.parametrize(
    "numerator",
    [True, False, 1.0, "1", None, object()],
)
def test_numerator_requires_strict_integer(
    numerator: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="numerator must be an integer",
    ):
        replace(
            create_result(),
            numerator=numerator,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "denominator",
    [True, False, 1.0, "1", None, object()],
)
def test_denominator_requires_strict_integer(
    denominator: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="denominator must be an integer",
    ):
        replace(
            create_result(),
            denominator=denominator,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("denominator", [0, -1, -(10**30)])
def test_denominator_requires_positive_value(
    denominator: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="denominator must be positive",
    ):
        create_result(
            numerator=1,
            denominator=denominator,
        )


@pytest.mark.parametrize(
    ("numerator", "denominator"),
    [
        (-(10**30), 1),
        (-5, 3),
        (-3, 5),
        (-1, 1),
        (0, 1),
        (1, 1),
        (3, 5),
        (5, 3),
        (10**30, 1),
    ],
)
def test_canonical_signed_ratios_are_accepted_exactly(
    numerator: int,
    denominator: int,
) -> None:
    result = create_result(
        numerator=numerator,
        denominator=denominator,
    )

    assert result.numerator == numerator
    assert result.denominator == denominator


@pytest.mark.parametrize(
    ("numerator", "denominator"),
    [(-10, 4), (-6, 10), (0, 2), (2, 4), (10, 4)],
)
def test_reducible_ratios_are_rejected(
    numerator: int,
    denominator: int,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "numerator and denominator must form a canonical "
            "irreducible ratio"
        ),
    ):
        create_result(
            numerator=numerator,
            denominator=denominator,
        )


def test_zero_has_one_canonical_representation() -> None:
    zero = create_result(numerator=0, denominator=1)

    assert (zero.numerator, zero.denominator) == (0, 1)

    with pytest.raises(ValueError):
        create_result(numerator=0, denominator=10)


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


def test_result_contains_no_amount_or_indeterminate_fields() -> None:
    field_names = {
        field.name
        for field in fields(RetailProductDerivedMarginRatio)
    }

    assert field_names.isdisjoint(
        {
            "margin_amount",
            "margin_percentage",
            "markup",
            "status",
            "reason",
        }
    )


def test_contract_does_not_calculate_or_select_denominator() -> None:
    module = inspect.getmodule(RetailProductDerivedMarginRatio)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))

    assert not any(
        isinstance(node, ast.BinOp)
        for node in ast.walk(tree)
    )

    numerator_negative_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Compare)
        and isinstance(node.left, ast.Attribute)
        and node.left.attr == "numerator"
        and any(
            isinstance(operator, (ast.Lt, ast.LtE))
            for operator in node.ops
        )
    ]
    assert not numerator_negative_checks


def test_contract_imports_no_external_or_execution_capability() -> None:
    module = inspect.getmodule(RetailProductDerivedMarginRatio)
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
            "decimal",
            "fractions",
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
    module = inspect.getmodule(RetailProductDerivedMarginRatio)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    function_names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert function_names == {"__post_init__"}
