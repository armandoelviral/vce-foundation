from dataclasses import FrozenInstanceError, fields, replace
from datetime import UTC, datetime, timedelta
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


def create_product_identity(
    *,
    product_id: str = "product-001",
) -> RetailProductIdentity:
    return RetailProductIdentity(
        product_id=product_id,
        sku=f"SKU-{product_id}",
        catalog_id="catalog-001",
        catalog_version=1,
    )


def create_context_scope(
    *,
    point_of_sale_id: str = "store-001",
) -> RetailContextScope:
    return RetailContextScope(
        context_id="context-001",
        commercial_channel_id="store",
        point_of_sale_id=point_of_sale_id,
        department_id="childrens-apparel",
        profile_version=1,
    )


def create_binding(
    *,
    context_scope: RetailContextScope,
    observation_id: str,
    observation_version: int = 1,
    dimension_id: str,
    dimension_type: str,
    observed_at: datetime = PERIOD_UNTIL,
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
        observation_version=observation_version,
        case_id="case-001",
        snapshot_id=snapshot_id,
        snapshot_version=1,
        dimension_id=dimension_id,
        source_identity=source_identity,
        observed_at=observed_at,
        recorded_at=observed_at,
        effective_from=min(PERIOD_FROM, observed_at),
        evidence_ids=(f"evidence-{observation_id}",),
    )
    return RetailContextObservationProvenanceBinding(
        snapshot=snapshot,
        dimension=dimension,
        provenance=provenance,
    )


def create_sales_observation(
    *,
    product_identity: RetailProductIdentity | None = None,
    context_scope: RetailContextScope | None = None,
) -> RetailProductObservedSalesQuantity:
    product_identity = product_identity or create_product_identity()
    context_scope = context_scope or create_context_scope()
    return RetailProductObservedSalesQuantity(
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


def create_inventory_observation(
    *,
    product_identity: RetailProductIdentity | None = None,
    context_scope: RetailContextScope | None = None,
    observation_id: str = "inventory-001",
    observation_version: int = 1,
    observed_at: datetime = PERIOD_UNTIL,
) -> RetailProductObservedInventory:
    product_identity = product_identity or create_product_identity()
    context_scope = context_scope or create_context_scope()
    return RetailProductObservedInventory(
        product_identity=product_identity,
        context_scope=context_scope,
        observed_quantity=20,
        quantity_unit=RetailInventoryQuantityUnit.UNIT,
        provenance_binding=create_binding(
            context_scope=context_scope,
            observation_id=observation_id,
            observation_version=observation_version,
            dimension_id=f"dimension-{observation_id}",
            dimension_type="PRODUCT_INVENTORY_QUANTITY",
            observed_at=observed_at,
        ),
    )


def create_basis(
    *,
    sales_observation: RetailProductObservedSalesQuantity | None = None,
    inventory_observations: tuple[
        RetailProductObservedInventory, ...
    ] | None = None,
) -> RetailProductSellThroughCalculationBasis:
    return RetailProductSellThroughCalculationBasis(
        sales_observation=(
            sales_observation or create_sales_observation()
        ),
        inventory_observations=(
            inventory_observations
            if inventory_observations is not None
            else (create_inventory_observation(),)
        ),
        calculation_scheme_id="sell-through-scheme-001",
        calculation_scheme_version=1,
    )


def test_calculation_basis_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(RetailProductSellThroughCalculationBasis)
    ) == (
        "sales_observation",
        "inventory_observations",
        "calculation_scheme_id",
        "calculation_scheme_version",
    )


def test_calculation_basis_is_immutable() -> None:
    basis = create_basis()

    with pytest.raises(FrozenInstanceError):
        basis.calculation_scheme_version = 2  # type: ignore[misc]


def test_calculation_basis_uses_slots() -> None:
    assert not hasattr(create_basis(), "__dict__")


def test_complete_observations_are_preserved() -> None:
    sales = create_sales_observation()
    inventories = (
        create_inventory_observation(observation_id="inventory-001"),
        create_inventory_observation(observation_id="inventory-002"),
    )
    basis = create_basis(
        sales_observation=sales,
        inventory_observations=inventories,
    )

    assert basis.sales_observation is sales
    assert basis.inventory_observations is inventories


def test_sales_observation_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "sales_observation must be a "
            "RetailProductObservedSalesQuantity"
        ),
    ):
        create_basis(
            sales_observation=object(),  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("inventories", [[], set(), object(), None])
def test_inventory_observations_requires_tuple(
    inventories: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="inventory_observations must be a tuple",
    ):
        RetailProductSellThroughCalculationBasis(
            sales_observation=create_sales_observation(),
            inventory_observations=inventories,  # type: ignore[arg-type]
            calculation_scheme_id="scheme-001",
            calculation_scheme_version=1,
        )


def test_inventory_observations_must_not_be_empty() -> None:
    with pytest.raises(
        ValueError,
        match="inventory_observations must not be empty",
    ):
        create_basis(inventory_observations=())


def test_every_inventory_observation_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "inventory_observation must be a "
            "RetailProductObservedInventory"
        ),
    ):
        create_basis(
            inventory_observations=(object(),),  # type: ignore[arg-type]
        )


def test_reconstructed_equal_product_identity_is_accepted() -> None:
    sales = create_sales_observation()
    reconstructed_product = replace(sales.product_identity)
    inventory = create_inventory_observation(
        product_identity=reconstructed_product,
    )

    basis = create_basis(
        sales_observation=sales,
        inventory_observations=(inventory,),
    )

    assert reconstructed_product == sales.product_identity
    assert reconstructed_product is not sales.product_identity
    assert basis.inventory_observations == (inventory,)


def test_different_product_identity_is_rejected() -> None:
    sales = create_sales_observation()
    inventory = create_inventory_observation(
        product_identity=create_product_identity(
            product_id="product-002",
        ),
    )

    with pytest.raises(
        ValueError,
        match="product_identity must match",
    ):
        create_basis(
            sales_observation=sales,
            inventory_observations=(inventory,),
        )


def test_reconstructed_equal_context_scope_is_accepted() -> None:
    sales = create_sales_observation()
    reconstructed_scope = replace(sales.context_scope)
    inventory = create_inventory_observation(
        context_scope=reconstructed_scope,
    )

    basis = create_basis(
        sales_observation=sales,
        inventory_observations=(inventory,),
    )

    assert reconstructed_scope == sales.context_scope
    assert reconstructed_scope is not sales.context_scope
    assert basis.inventory_observations == (inventory,)


def test_different_context_scope_is_rejected() -> None:
    sales = create_sales_observation()
    inventory = create_inventory_observation(
        context_scope=create_context_scope(
            point_of_sale_id="store-002",
        ),
    )

    with pytest.raises(
        ValueError,
        match="context_scope must match",
    ):
        create_basis(
            sales_observation=sales,
            inventory_observations=(inventory,),
        )


def test_duplicate_inventory_observation_object_is_rejected() -> None:
    inventory = create_inventory_observation()

    with pytest.raises(
        ValueError,
        match="duplicate inventory observation identity",
    ):
        create_basis(
            inventory_observations=(inventory, inventory),
        )


def test_reconstructed_duplicate_observation_identity_is_rejected() -> None:
    first = create_inventory_observation()
    second = create_inventory_observation()

    assert first is not second

    with pytest.raises(
        ValueError,
        match="duplicate inventory observation identity",
    ):
        create_basis(inventory_observations=(first, second))


def test_distinct_observation_versions_are_preserved() -> None:
    inventories = (
        create_inventory_observation(observation_version=1),
        create_inventory_observation(observation_version=2),
    )

    basis = create_basis(inventory_observations=inventories)

    assert basis.inventory_observations == inventories


@pytest.mark.parametrize("scheme_id", [None, 1, True, (), object()])
def test_calculation_scheme_id_requires_string(
    scheme_id: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="calculation_scheme_id must be a string",
    ):
        replace(
            create_basis(),
            calculation_scheme_id=scheme_id,  # type: ignore[arg-type]
        )


def test_calculation_scheme_id_must_not_be_empty() -> None:
    with pytest.raises(
        ValueError,
        match="calculation_scheme_id must not be empty",
    ):
        replace(create_basis(), calculation_scheme_id="")


@pytest.mark.parametrize("version", [True, False, 1.0, "1", None])
def test_calculation_scheme_version_requires_strict_integer(
    version: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="calculation_scheme_version must be an integer",
    ):
        replace(
            create_basis(),
            calculation_scheme_version=version,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("version", [0, -1])
def test_calculation_scheme_version_must_be_positive(
    version: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="calculation_scheme_version must be positive",
    ):
        replace(
            create_basis(),
            calculation_scheme_version=version,
        )


def test_inventory_temporal_roles_are_not_inferred() -> None:
    inventories = (
        create_inventory_observation(
            observation_id="inventory-before",
            observed_at=PERIOD_FROM - timedelta(days=1),
        ),
        create_inventory_observation(
            observation_id="inventory-after",
            observed_at=PERIOD_UNTIL + timedelta(days=1),
        ),
    )

    basis = create_basis(inventory_observations=inventories)

    assert basis.inventory_observations == inventories


def test_contract_introduces_no_result_or_formula() -> None:
    names = {
        field.name
        for field in fields(RetailProductSellThroughCalculationBasis)
    }
    forbidden_names = {
        "sell_through_value",
        "numerator",
        "denominator",
        "opening_inventory",
        "closing_inventory",
        "average_inventory",
        "percentage",
    }

    assert names.isdisjoint(forbidden_names)

    module = inspect.getmodule(
        RetailProductSellThroughCalculationBasis
    )
    assert module is not None
    source = inspect.getsource(module).lower()

    for forbidden_term in (
        "requests",
        "notion",
        "openai",
        "subprocess",
        "recommend",
        "priorit",
    ):
        assert forbidden_term not in source
