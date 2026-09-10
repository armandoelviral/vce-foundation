from dataclasses import FrozenInstanceError, fields, replace
from datetime import UTC, datetime, timedelta, timezone
import inspect

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.retail_commercial_observation_period import (
    RetailCommercialObservationPeriod,
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
from sp001.contracts.retail_product_indeterminate_sell_through_result import (
    RetailProductIndeterminateSellThroughResult,
    RetailProductSellThroughIndeterminacyReason,
)
from sp001.contracts.retail_product_observed_inventory import (
    RetailInventoryQuantityUnit,
    RetailProductObservedInventory,
)
from sp001.contracts.retail_product_observed_sales_quantity import (
    RetailCommercialQuantityUnit,
    RetailProductObservedSalesQuantity,
)
from sp001.contracts.retail_product_sell_through_calculation_basis import (
    RetailProductSellThroughCalculationBasis,
)


PERIOD_FROM = datetime(2026, 9, 1, tzinfo=UTC)
PERIOD_UNTIL = datetime(2026, 9, 8, tzinfo=UTC)
DETERMINED_AT = datetime(2026, 9, 8, 1, tzinfo=UTC)


def create_context_scope() -> RetailContextScope:
    return RetailContextScope(
        context_id="context-001",
        commercial_channel_id="store",
        point_of_sale_id="store-001",
        department_id="childrens-apparel",
        profile_version=1,
    )


def create_product_identity() -> RetailProductIdentity:
    return RetailProductIdentity(
        product_id="product-001",
        sku="SKU-001",
        catalog_id="catalog-001",
        catalog_version=1,
    )


def create_binding(
    *,
    context_scope: RetailContextScope,
    observation_id: str,
    dimension_id: str,
    dimension_type: str,
) -> RetailContextObservationProvenanceBinding:
    dimension = RetailContextDimension(
        dimension_id=dimension_id,
        dimension_type=dimension_type,
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.MEASURED,
        value="0 UNIT",
    )
    snapshot_id = f"snapshot-{observation_id}"
    snapshot = RetailContextSnapshot(
        snapshot_id=snapshot_id,
        snapshot_version=1,
        case_id="case-001",
        dimensions=(dimension,),
        context_scope=context_scope,
    )
    source_identity = KnowledgeSourceIdentity(
        source_id=f"source-{observation_id}",
        source_version="1",
        source_content_digest=KnowledgeContentDigest(
            algorithm="SHA-256",
            value="0" * 64,
        ),
    )
    provenance = RetailContextObservationProvenance(
        observation_id=observation_id,
        observation_version=1,
        case_id="case-001",
        snapshot_id=snapshot_id,
        snapshot_version=1,
        dimension_id=dimension_id,
        source_identity=source_identity,
        observed_at=PERIOD_UNTIL,
        recorded_at=PERIOD_UNTIL,
        effective_from=PERIOD_FROM,
        evidence_ids=(f"evidence-{observation_id}",),
    )
    return RetailContextObservationProvenanceBinding(
        snapshot=snapshot,
        dimension=dimension,
        provenance=provenance,
    )


def create_basis() -> RetailProductSellThroughCalculationBasis:
    context_scope = create_context_scope()
    product_identity = create_product_identity()
    sales = RetailProductObservedSalesQuantity(
        product_identity=product_identity,
        context_scope=context_scope,
        observation_period=RetailCommercialObservationPeriod(
            period_id="period-001",
            period_version=1,
            period_from=PERIOD_FROM,
            period_until=PERIOD_UNTIL,
        ),
        sold_quantity=10,
        quantity_unit=RetailCommercialQuantityUnit.UNIT,
        measurement_scheme_id="sales-measurement-001",
        measurement_scheme_version=1,
        provenance_binding=create_binding(
            context_scope=context_scope,
            observation_id="sales-001",
            dimension_id="sales-dimension-001",
            dimension_type="PRODUCT_SALES_QUANTITY",
        ),
    )
    inventory = RetailProductObservedInventory(
        product_identity=product_identity,
        context_scope=context_scope,
        observed_quantity=20,
        quantity_unit=RetailInventoryQuantityUnit.UNIT,
        provenance_binding=create_binding(
            context_scope=context_scope,
            observation_id="inventory-001",
            dimension_id="inventory-dimension-001",
            dimension_type="PRODUCT_INVENTORY_QUANTITY",
        ),
    )
    return RetailProductSellThroughCalculationBasis(
        sales_observation=sales,
        inventory_observations=(inventory,),
        calculation_scheme_id="sell-through-scheme-001",
        calculation_scheme_version=1,
    )


def create_result(
    *,
    reason: RetailProductSellThroughIndeterminacyReason = (
        RetailProductSellThroughIndeterminacyReason
        .UNSUPPORTED_CALCULATION_SCHEME
    ),
    determined_at: datetime = DETERMINED_AT,
) -> RetailProductIndeterminateSellThroughResult:
    return RetailProductIndeterminateSellThroughResult(
        result_id="indeterminate-result-001",
        result_version=1,
        calculation_basis=create_basis(),
        reason=reason,
        determined_at=determined_at,
    )


def test_indeterminacy_reason_vocabulary_is_exact() -> None:
    assert tuple(RetailProductSellThroughIndeterminacyReason) == (
        RetailProductSellThroughIndeterminacyReason
        .UNSUPPORTED_CALCULATION_SCHEME,
        RetailProductSellThroughIndeterminacyReason
        .INSUFFICIENT_INPUT_EVIDENCE,
        RetailProductSellThroughIndeterminacyReason
        .NONPOSITIVE_DENOMINATOR,
    )


def test_indeterminate_result_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(RetailProductIndeterminateSellThroughResult)
    ) == (
        "result_id",
        "result_version",
        "calculation_basis",
        "reason",
        "determined_at",
    )


def test_indeterminate_result_is_immutable() -> None:
    result = create_result()

    with pytest.raises(FrozenInstanceError):
        result.result_version = 2  # type: ignore[misc]


def test_indeterminate_result_uses_slots() -> None:
    assert not hasattr(create_result(), "__dict__")


def test_complete_calculation_basis_is_preserved() -> None:
    basis = create_basis()
    result = replace(create_result(), calculation_basis=basis)

    assert result.calculation_basis is basis


@pytest.mark.parametrize("result_id", [None, 1, True, (), object()])
def test_result_id_requires_string(result_id: object) -> None:
    with pytest.raises(TypeError, match="result_id must be a string"):
        replace(
            create_result(),
            result_id=result_id,  # type: ignore[arg-type]
        )


def test_result_id_must_not_be_empty() -> None:
    with pytest.raises(ValueError, match="result_id must not be empty"):
        replace(create_result(), result_id="")


@pytest.mark.parametrize("version", [True, False, 1.0, "1", None])
def test_result_version_requires_strict_integer(version: object) -> None:
    with pytest.raises(
        TypeError,
        match="result_version must be an integer",
    ):
        replace(
            create_result(),
            result_version=version,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("version", [0, -1])
def test_result_version_must_be_positive(version: int) -> None:
    with pytest.raises(
        ValueError,
        match="result_version must be positive",
    ):
        replace(create_result(), result_version=version)


def test_calculation_basis_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "calculation_basis must be a "
            "RetailProductSellThroughCalculationBasis"
        ),
    ):
        replace(
            create_result(),
            calculation_basis=object(),  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "reason",
    tuple(RetailProductSellThroughIndeterminacyReason),
)
def test_each_declared_indeterminacy_reason_is_accepted(
    reason: RetailProductSellThroughIndeterminacyReason,
) -> None:
    result = create_result(reason=reason)

    assert result.reason is reason


@pytest.mark.parametrize(
    "reason",
    [
        "UNSUPPORTED_CALCULATION_SCHEME",
        "INSUFFICIENT_INPUT_EVIDENCE",
        "NONPOSITIVE_DENOMINATOR",
        None,
        object(),
    ],
)
def test_reason_requires_exact_enum(reason: object) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "reason must be a "
            "RetailProductSellThroughIndeterminacyReason"
        ),
    ):
        replace(
            create_result(),
            reason=reason,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("determined_at", [None, "2026-09-08", 0, object()])
def test_determined_at_requires_datetime(determined_at: object) -> None:
    with pytest.raises(
        TypeError,
        match="determined_at must be a datetime",
    ):
        replace(
            create_result(),
            determined_at=determined_at,  # type: ignore[arg-type]
        )


def test_determined_at_requires_timezone_awareness() -> None:
    with pytest.raises(
        ValueError,
        match="determined_at must be timezone-aware",
    ):
        create_result(
            determined_at=datetime(2026, 9, 8, 1),
        )


def test_aware_determined_at_is_preserved_without_normalization() -> None:
    declared = datetime(
        2026,
        9,
        7,
        20,
        tzinfo=timezone(-timedelta(hours=5)),
    )
    result = create_result(determined_at=declared)

    assert result.determined_at is declared
    assert result.determined_at.utcoffset() == timedelta(hours=-5)


def test_determined_at_order_is_not_inferred() -> None:
    declared = PERIOD_FROM - timedelta(days=1)
    result = create_result(determined_at=declared)

    assert result.determined_at == declared


def test_successful_ratio_fields_are_absent() -> None:
    field_names = {
        field.name
        for field in fields(RetailProductIndeterminateSellThroughResult)
    }

    assert field_names.isdisjoint(
        {
            "numerator",
            "denominator",
            "ratio",
            "percentage",
        }
    )


def test_contract_introduces_no_calculation_or_external_capability() -> None:
    module = inspect.getmodule(
        RetailProductIndeterminateSellThroughResult
    )
    assert module is not None
    source = inspect.getsource(module).lower()

    for forbidden_term in (
        "numerator:",
        "denominator:",
        "percentage",
        "round(",
        "decimal",
        "except ",
        "recommend",
        "priorit",
        "requests",
        "notion",
        "openai",
        "subprocess",
    ):
        assert forbidden_term not in source
