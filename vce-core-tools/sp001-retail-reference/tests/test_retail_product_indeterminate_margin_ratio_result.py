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
from sp001.contracts.retail_product_indeterminate_margin_ratio_result import (
    RetailProductIndeterminateMarginRatioResult,
    RetailProductMarginRatioIndeterminacyReason,
)
from sp001.contracts.retail_product_margin_calculation_basis import (
    RetailProductMarginCalculationBasis,
)
from sp001.contracts.retail_product_observed_cost import (
    RetailProductObservedCost,
)
from sp001.contracts.retail_product_observed_price import (
    RetailProductObservedPrice,
)


OBSERVED_AT = datetime(2026, 9, 10, 12, 0, tzinfo=UTC)
DETERMINED_AT = datetime(2026, 9, 10, 13, 0, tzinfo=UTC)


def create_binding(
    context_scope: RetailContextScope,
    kind: str,
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
    provenance = RetailContextObservationProvenance(
        observation_id=f"{kind}-observation-001",
        observation_version=1,
        case_id="case-001",
        snapshot_id=snapshot_id,
        snapshot_version=1,
        dimension_id=dimension_id,
        source_identity=KnowledgeSourceIdentity(
            source_id=f"{kind}-source-001",
            source_version="1",
            source_content_digest=KnowledgeContentDigest(
                algorithm="SHA-256",
                value=("0" if kind == "price" else "1") * 64,
            ),
        ),
        observed_at=OBSERVED_AT,
        recorded_at=OBSERVED_AT,
        effective_from=OBSERVED_AT,
        evidence_ids=(f"{kind}-evidence-001",),
    )
    return RetailContextObservationProvenanceBinding(
        snapshot=snapshot,
        dimension=dimension,
        provenance=provenance,
    )


def create_basis() -> RetailProductMarginCalculationBasis:
    product = RetailProductIdentity(
        product_id="product-001",
        sku="SKU-001",
        catalog_id="catalog-001",
        catalog_version=1,
    )
    context = RetailContextScope(
        context_id="context-001",
        commercial_channel_id="store",
        point_of_sale_id="store-001",
        department_id="childrens-apparel",
        profile_version=1,
    )
    currency = RetailCommercialCurrencyIdentity(
        currency_code="MXN",
        currency_scheme_id="ISO-4217",
        currency_scheme_version=1,
    )
    price = RetailProductObservedPrice(
        product_identity=product,
        context_scope=context,
        monetary_amount=RetailCommercialMonetaryAmount(currency, 15000),
        pricing_scheme_id="observed-store-price",
        pricing_scheme_version=1,
        provenance_binding=create_binding(context, "price"),
    )
    cost = RetailProductObservedCost(
        product_identity=product,
        context_scope=context,
        monetary_amount=RetailCommercialMonetaryAmount(currency, 9000),
        costing_scheme_id="observed-product-cost",
        costing_scheme_version=1,
        provenance_binding=create_binding(context, "cost"),
    )
    return RetailProductMarginCalculationBasis(
        price_observation=price,
        cost_observation=cost,
        calculation_scheme_id="declared-margin-method",
        calculation_scheme_version=1,
    )


def create_result(
    reason: RetailProductMarginRatioIndeterminacyReason = (
        RetailProductMarginRatioIndeterminacyReason
        .INSUFFICIENT_INPUT_EVIDENCE
    ),
    determined_at: datetime = DETERMINED_AT,
) -> RetailProductIndeterminateMarginRatioResult:
    return RetailProductIndeterminateMarginRatioResult(
        result_id="indeterminate-margin-ratio-001",
        result_version=1,
        calculation_basis=create_basis(),
        reason=reason,
        determined_at=determined_at,
    )


def test_reason_vocabulary_is_exact() -> None:
    assert tuple(reason.value for reason in RetailProductMarginRatioIndeterminacyReason) == (
        "UNSUPPORTED_CALCULATION_SCHEME",
        "INSUFFICIENT_INPUT_EVIDENCE",
        "NONPOSITIVE_DENOMINATOR",
    )


def test_result_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(RetailProductIndeterminateMarginRatioResult)) == (
        "result_id",
        "result_version",
        "calculation_basis",
        "reason",
        "determined_at",
    )


def test_result_is_frozen_and_slotted() -> None:
    result = create_result()
    assert not hasattr(result, "__dict__")
    with pytest.raises(FrozenInstanceError):
        result.reason = RetailProductMarginRatioIndeterminacyReason.UNSUPPORTED_CALCULATION_SCHEME  # type: ignore[misc]


def test_calculation_basis_reference_is_preserved() -> None:
    basis = create_basis()
    result = replace(create_result(), calculation_basis=basis)
    assert result.calculation_basis is basis


@pytest.mark.parametrize("value", [None, 1, True, object()])
def test_result_id_requires_string(value: object) -> None:
    with pytest.raises(TypeError, match="result_id must be a string"):
        replace(create_result(), result_id=value)  # type: ignore[arg-type]


def test_empty_result_id_is_rejected() -> None:
    with pytest.raises(ValueError, match="result_id must not be empty"):
        replace(create_result(), result_id="")


@pytest.mark.parametrize("value", [" ", "\t", " result id "])
def test_result_id_remains_literal(value: str) -> None:
    assert replace(create_result(), result_id=value).result_id == value


@pytest.mark.parametrize("value", [True, False, 1.0, "1", None])
def test_result_version_requires_strict_integer(value: object) -> None:
    with pytest.raises(TypeError, match="result_version must be an integer"):
        replace(create_result(), result_version=value)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [0, -1, -(10**30)])
def test_result_version_requires_positive_value(value: int) -> None:
    with pytest.raises(ValueError, match="result_version must be positive"):
        replace(create_result(), result_version=value)


def test_calculation_basis_requires_exact_type() -> None:
    with pytest.raises(TypeError, match="calculation_basis must be a RetailProductMarginCalculationBasis"):
        replace(create_result(), calculation_basis=object())  # type: ignore[arg-type]


@pytest.mark.parametrize("reason", tuple(RetailProductMarginRatioIndeterminacyReason))
def test_each_typed_reason_is_accepted(reason: RetailProductMarginRatioIndeterminacyReason) -> None:
    assert create_result(reason=reason).reason is reason


@pytest.mark.parametrize("value", ["INSUFFICIENT_INPUT_EVIDENCE", None, object()])
def test_reason_requires_exact_enum_type(value: object) -> None:
    with pytest.raises(TypeError, match="reason must be a RetailProductMarginRatioIndeterminacyReason"):
        replace(create_result(), reason=value)  # type: ignore[arg-type]


def test_denominator_reason_is_ratio_specific() -> None:
    assert (
        RetailProductMarginRatioIndeterminacyReason
        .NONPOSITIVE_DENOMINATOR.value
        == "NONPOSITIVE_DENOMINATOR"
    )


@pytest.mark.parametrize("value", [None, "2026-09-10T13:00:00Z", 0, object()])
def test_determined_at_requires_datetime(value: object) -> None:
    with pytest.raises(TypeError, match="determined_at must be a datetime"):
        replace(create_result(), determined_at=value)  # type: ignore[arg-type]


def test_determined_at_requires_timezone_awareness() -> None:
    with pytest.raises(ValueError, match="determined_at must be timezone-aware"):
        create_result(determined_at=datetime(2026, 9, 10, 13, 0))


def test_successful_result_fields_are_absent() -> None:
    names = {field.name for field in fields(RetailProductIndeterminateMarginRatioResult)}
    assert names.isdisjoint({"margin_amount", "numerator", "denominator", "margin_percentage", "status"})


def test_contract_performs_no_calculation_or_exception_mapping() -> None:
    module = inspect.getmodule(RetailProductIndeterminateMarginRatioResult)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    assert not any(isinstance(node, (ast.BinOp, ast.Try)) for node in ast.walk(tree))


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(RetailProductIndeterminateMarginRatioResult)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    roots.update(
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    )
    assert roots.isdisjoint({"os", "pathlib", "subprocess", "sqlite3", "requests", "httpx", "urllib", "openai", "notion_client"})


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(RetailProductIndeterminateMarginRatioResult)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert names == {"__post_init__"}
