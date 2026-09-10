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
from sp001.contracts.retail_product_derived_sell_through_ratio import (
    RetailProductDerivedSellThroughRatio,
)
from sp001.contracts.retail_product_identity import RetailProductIdentity
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
DERIVED_AT = datetime(2026, 9, 8, 1, tzinfo=UTC)


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
    product_identity = create_product_identity()
    context_scope = create_context_scope()
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


def create_ratio(
    *,
    numerator: int = 1,
    denominator: int = 2,
    derived_at: datetime = DERIVED_AT,
) -> RetailProductDerivedSellThroughRatio:
    return RetailProductDerivedSellThroughRatio(
        result_id="sell-through-result-001",
        result_version=1,
        calculation_basis=create_basis(),
        numerator=numerator,
        denominator=denominator,
        derived_at=derived_at,
    )


def test_derived_ratio_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(RetailProductDerivedSellThroughRatio)
    ) == (
        "result_id",
        "result_version",
        "calculation_basis",
        "numerator",
        "denominator",
        "derived_at",
    )


def test_derived_ratio_is_immutable() -> None:
    ratio = create_ratio()

    with pytest.raises(FrozenInstanceError):
        ratio.numerator = 2  # type: ignore[misc]


def test_derived_ratio_uses_slots() -> None:
    assert not hasattr(create_ratio(), "__dict__")


def test_complete_calculation_basis_is_preserved() -> None:
    basis = create_basis()
    ratio = replace(create_ratio(), calculation_basis=basis)

    assert ratio.calculation_basis is basis


@pytest.mark.parametrize("result_id", [None, 1, True, (), object()])
def test_result_id_requires_string(result_id: object) -> None:
    with pytest.raises(TypeError, match="result_id must be a string"):
        replace(
            create_ratio(),
            result_id=result_id,  # type: ignore[arg-type]
        )


def test_result_id_must_not_be_empty() -> None:
    with pytest.raises(ValueError, match="result_id must not be empty"):
        replace(create_ratio(), result_id="")


@pytest.mark.parametrize("version", [True, False, 1.0, "1", None])
def test_result_version_requires_strict_integer(version: object) -> None:
    with pytest.raises(
        TypeError,
        match="result_version must be an integer",
    ):
        replace(
            create_ratio(),
            result_version=version,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("version", [0, -1])
def test_result_version_must_be_positive(version: int) -> None:
    with pytest.raises(
        ValueError,
        match="result_version must be positive",
    ):
        replace(create_ratio(), result_version=version)


def test_calculation_basis_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "calculation_basis must be a "
            "RetailProductSellThroughCalculationBasis"
        ),
    ):
        replace(
            create_ratio(),
            calculation_basis=object(),  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("numerator", [True, False, 1.0, "1", None])
def test_numerator_requires_strict_integer(numerator: object) -> None:
    with pytest.raises(TypeError, match="numerator must be an integer"):
        replace(
            create_ratio(),
            numerator=numerator,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("numerator", [-1, -100])
def test_numerator_must_not_be_negative(numerator: int) -> None:
    with pytest.raises(
        ValueError,
        match="numerator must not be negative",
    ):
        replace(create_ratio(), numerator=numerator)


@pytest.mark.parametrize("denominator", [True, False, 1.0, "1", None])
def test_denominator_requires_strict_integer(
    denominator: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="denominator must be an integer",
    ):
        replace(
            create_ratio(),
            denominator=denominator,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("denominator", [0, -1, -100])
def test_denominator_must_be_positive(denominator: int) -> None:
    with pytest.raises(
        ValueError,
        match="denominator must be positive",
    ):
        replace(create_ratio(), denominator=denominator)


@pytest.mark.parametrize(
    ("numerator", "denominator"),
    [(0, 1), (1, 2), (1, 1), (2, 1), (3, 2), (17, 31)],
)
def test_canonical_exact_ratios_are_accepted(
    numerator: int,
    denominator: int,
) -> None:
    ratio = create_ratio(
        numerator=numerator,
        denominator=denominator,
    )

    assert ratio.numerator == numerator
    assert ratio.denominator == denominator


@pytest.mark.parametrize(
    ("numerator", "denominator"),
    [(0, 2), (2, 4), (6, 3), (12, 8)],
)
def test_reducible_ratios_are_rejected(
    numerator: int,
    denominator: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="canonical irreducible ratio",
    ):
        create_ratio(
            numerator=numerator,
            denominator=denominator,
        )


def test_ratio_above_one_is_accepted() -> None:
    ratio = create_ratio(numerator=5, denominator=2)

    assert ratio.numerator > ratio.denominator


def test_zero_has_one_canonical_representation() -> None:
    assert create_ratio(numerator=0, denominator=1).numerator == 0

    with pytest.raises(ValueError, match="canonical irreducible ratio"):
        create_ratio(numerator=0, denominator=10)


@pytest.mark.parametrize("derived_at", [None, "2026-09-08", 0, object()])
def test_derived_at_requires_datetime(derived_at: object) -> None:
    with pytest.raises(TypeError, match="derived_at must be a datetime"):
        replace(
            create_ratio(),
            derived_at=derived_at,  # type: ignore[arg-type]
        )


def test_derived_at_requires_timezone_awareness() -> None:
    with pytest.raises(
        ValueError,
        match="derived_at must be timezone-aware",
    ):
        create_ratio(derived_at=datetime(2026, 9, 8, 1))


def test_aware_derived_at_is_preserved_without_normalization() -> None:
    declared = datetime(
        2026,
        9,
        7,
        20,
        tzinfo=timezone(-timedelta(hours=5)),
    )
    ratio = create_ratio(derived_at=declared)

    assert ratio.derived_at is declared
    assert ratio.derived_at.utcoffset() == timedelta(hours=-5)


def test_result_does_not_require_derivation_after_inputs() -> None:
    declared = PERIOD_FROM - timedelta(days=1)
    ratio = create_ratio(derived_at=declared)

    assert ratio.derived_at == declared


def test_contract_introduces_no_formula_or_presentation() -> None:
    module = inspect.getmodule(RetailProductDerivedSellThroughRatio)
    assert module is not None
    source = inspect.getsource(module).lower()

    for forbidden_term in (
        "percentage",
        "percent",
        "round(",
        "decimal",
        "opening_inventory",
        "closing_inventory",
        "average_inventory",
        "recommend",
        "priorit",
        "requests",
        "notion",
        "openai",
        "subprocess",
    ):
        assert forbidden_term not in source
