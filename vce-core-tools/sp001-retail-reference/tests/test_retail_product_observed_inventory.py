from dataclasses import FrozenInstanceError, fields, replace
from datetime import UTC, datetime
import inspect

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
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


OBSERVED_AT = datetime(2026, 9, 5, 12, 0, tzinfo=UTC)


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


def create_provenance_binding(
    *,
    context_scope: RetailContextScope | None,
) -> RetailContextObservationProvenanceBinding:
    dimension = RetailContextDimension(
        dimension_id="inventory-observation-001",
        dimension_type="PRODUCT_INVENTORY",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.MEASURED,
        value="0 UNIT",
    )
    snapshot = RetailContextSnapshot(
        snapshot_id="snapshot-001",
        snapshot_version=1,
        case_id="case-001",
        dimensions=(dimension,),
        context_scope=context_scope,
    )
    source_identity = KnowledgeSourceIdentity(
        source_id="inventory-source-001",
        source_version="1",
        source_content_digest=KnowledgeContentDigest(
            algorithm="SHA-256",
            value="0" * 64,
        ),
    )
    provenance = RetailContextObservationProvenance(
        observation_id="observation-001",
        observation_version=1,
        case_id="case-001",
        snapshot_id="snapshot-001",
        snapshot_version=1,
        dimension_id="inventory-observation-001",
        source_identity=source_identity,
        observed_at=OBSERVED_AT,
        recorded_at=OBSERVED_AT,
        effective_from=OBSERVED_AT,
        evidence_ids=("evidence-001",),
    )
    return RetailContextObservationProvenanceBinding(
        snapshot=snapshot,
        dimension=dimension,
        provenance=provenance,
    )


def create_observed_inventory(
    *,
    observed_quantity: int = 0,
) -> RetailProductObservedInventory:
    context_scope = create_context_scope()
    return RetailProductObservedInventory(
        product_identity=create_product_identity(),
        context_scope=context_scope,
        observed_quantity=observed_quantity,
        quantity_unit=RetailInventoryQuantityUnit.UNIT,
        provenance_binding=create_provenance_binding(
            context_scope=context_scope,
        ),
    )


def test_quantity_unit_vocabulary_is_exact() -> None:
    assert tuple(RetailInventoryQuantityUnit) == (
        RetailInventoryQuantityUnit.UNIT,
    )
    assert RetailInventoryQuantityUnit.UNIT.value == "UNIT"


def test_observed_inventory_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(RetailProductObservedInventory)
    ) == (
        "product_identity",
        "context_scope",
        "observed_quantity",
        "quantity_unit",
        "provenance_binding",
    )


def test_observed_inventory_is_immutable() -> None:
    inventory = create_observed_inventory()

    with pytest.raises(FrozenInstanceError):
        inventory.observed_quantity = 1  # type: ignore[misc]


def test_observed_inventory_uses_slots() -> None:
    assert not hasattr(
        create_observed_inventory(),
        "__dict__",
    )


@pytest.mark.parametrize(
    "observed_quantity",
    [0, 1, 100],
)
def test_observed_inventory_accepts_nonnegative_integer_quantity(
    observed_quantity: int,
) -> None:
    inventory = create_observed_inventory(
        observed_quantity=observed_quantity,
    )

    assert inventory.observed_quantity == observed_quantity


@pytest.mark.parametrize(
    "observed_quantity",
    [True, False, 0.0, "1", None],
)
def test_observed_quantity_requires_strict_integer(
    observed_quantity: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="observed_quantity must be an integer",
    ):
        create_observed_inventory(
            observed_quantity=observed_quantity,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "observed_quantity",
    [-1, -100],
)
def test_observed_quantity_rejects_negative_integer(
    observed_quantity: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="observed_quantity must not be negative",
    ):
        create_observed_inventory(
            observed_quantity=observed_quantity,
        )


def test_product_identity_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match="product_identity must be a RetailProductIdentity",
    ):
        replace(
            create_observed_inventory(),
            product_identity=object(),
        )


def test_context_scope_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match="context_scope must be a RetailContextScope",
    ):
        replace(
            create_observed_inventory(),
            context_scope=object(),
        )


def test_quantity_unit_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "quantity_unit must be a "
            "RetailInventoryQuantityUnit"
        ),
    ):
        replace(
            create_observed_inventory(),
            quantity_unit="UNIT",
        )


def test_provenance_binding_requires_exact_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "provenance_binding must be a "
            "RetailContextObservationProvenanceBinding"
        ),
    ):
        replace(
            create_observed_inventory(),
            provenance_binding=object(),
        )


def test_exact_snapshot_context_scope_reference_is_preserved() -> None:
    inventory = create_observed_inventory()

    assert (
        inventory.provenance_binding.snapshot.context_scope
        is inventory.context_scope
    )


def test_equal_foreign_context_scope_is_rejected() -> None:
    inventory = create_observed_inventory()
    equal_foreign_scope = replace(inventory.context_scope)

    assert equal_foreign_scope == inventory.context_scope
    assert equal_foreign_scope is not inventory.context_scope

    with pytest.raises(
        ValueError,
        match="context_scope does not match provenance snapshot",
    ):
        replace(
            inventory,
            context_scope=equal_foreign_scope,
        )


def test_snapshot_without_context_scope_is_rejected() -> None:
    context_scope = create_context_scope()

    with pytest.raises(
        ValueError,
        match="context_scope does not match provenance snapshot",
    ):
        RetailProductObservedInventory(
            product_identity=create_product_identity(),
            context_scope=context_scope,
            observed_quantity=0,
            quantity_unit=RetailInventoryQuantityUnit.UNIT,
            provenance_binding=create_provenance_binding(
                context_scope=None,
            ),
        )


def test_snapshot_identity_and_version_are_not_duplicated() -> None:
    field_names = {
        field.name
        for field in fields(RetailProductObservedInventory)
    }

    assert "snapshot_id" not in field_names
    assert "snapshot_version" not in field_names
    assert "case_id" not in field_names
    assert "dimension_id" not in field_names


def test_zero_quantity_remains_an_uninterpreted_observation() -> None:
    inventory = create_observed_inventory(
        observed_quantity=0,
    )

    assert inventory.observed_quantity == 0
    assert not hasattr(inventory, "availability")
    assert not hasattr(inventory, "is_available")
    assert not hasattr(inventory, "stock_status")


def test_contract_adds_no_inventory_aggregation_or_flow_fields() -> None:
    field_names = {
        field.name
        for field in fields(RetailProductObservedInventory)
    }

    assert field_names.isdisjoint(
        {
            "sales_floor_quantity",
            "stockroom_quantity",
            "reserved_quantity",
            "in_transit_quantity",
            "ordered_quantity",
        }
    )


def test_contract_adds_no_commercial_decision_or_io_capability() -> None:
    source = inspect.getsource(
        __import__(
            "sp001.contracts.retail_product_observed_inventory",
            fromlist=["*"],
        )
    ).lower()

    forbidden = (
        "sell_through",
        "margin",
        "substitute",
        "recommend",
        "priorit",
        "requests",
        "notion",
        "openai",
        "subprocess",
        "pathlib",
    )

    assert all(
        term not in source
        for term in forbidden
    )
