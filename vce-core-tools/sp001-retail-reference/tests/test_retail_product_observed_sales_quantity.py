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
from sp001.contracts.retail_product_observed_sales_quantity import (
    RetailCommercialQuantityUnit,
    RetailProductObservedSalesQuantity,
)


PERIOD_FROM = datetime(2026, 9, 1, 0, 0, tzinfo=UTC)
PERIOD_UNTIL = datetime(2026, 9, 8, 0, 0, tzinfo=UTC)


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


def create_period() -> RetailCommercialObservationPeriod:
    return RetailCommercialObservationPeriod(
        period_id="sales-period-001",
        period_version=1,
        period_from=PERIOD_FROM,
        period_until=PERIOD_UNTIL,
    )


def create_binding(
    *,
    context_scope: RetailContextScope | None,
    observed_at: datetime = PERIOD_UNTIL,
) -> RetailContextObservationProvenanceBinding:
    dimension = RetailContextDimension(
        dimension_id="sales-observation-001",
        dimension_type="PRODUCT_SALES_QUANTITY",
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
        source_id="sales-source-001",
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
        dimension_id="sales-observation-001",
        source_identity=source_identity,
        observed_at=observed_at,
        recorded_at=observed_at,
        effective_from=PERIOD_FROM,
        evidence_ids=("evidence-001",),
    )
    return RetailContextObservationProvenanceBinding(
        snapshot=snapshot,
        dimension=dimension,
        provenance=provenance,
    )


def create_sales_quantity(
    *,
    sold_quantity: int = 0,
) -> RetailProductObservedSalesQuantity:
    context_scope = create_context_scope()
    return RetailProductObservedSalesQuantity(
        product_identity=create_product_identity(),
        context_scope=context_scope,
        observation_period=create_period(),
        sold_quantity=sold_quantity,
        quantity_unit=RetailCommercialQuantityUnit.UNIT,
        measurement_scheme_id="sales-measurement-001",
        measurement_scheme_version=1,
        provenance_binding=create_binding(
            context_scope=context_scope,
        ),
    )


def test_commercial_quantity_unit_vocabulary_is_exact() -> None:
    assert tuple(RetailCommercialQuantityUnit) == (
        RetailCommercialQuantityUnit.UNIT,
    )
    assert RetailCommercialQuantityUnit.UNIT.value == "UNIT"


def test_observed_sales_quantity_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(RetailProductObservedSalesQuantity)
    ) == (
        "product_identity",
        "context_scope",
        "observation_period",
        "sold_quantity",
        "quantity_unit",
        "measurement_scheme_id",
        "measurement_scheme_version",
        "provenance_binding",
    )


def test_observed_sales_quantity_is_immutable() -> None:
    observation = create_sales_quantity()

    with pytest.raises(FrozenInstanceError):
        observation.sold_quantity = 1  # type: ignore[misc]


def test_observed_sales_quantity_uses_slots() -> None:
    assert not hasattr(create_sales_quantity(), "__dict__")


def test_observation_preserves_exact_typed_references() -> None:
    observation = create_sales_quantity()

    assert observation.product_identity is not None
    assert observation.context_scope is (
        observation.provenance_binding.snapshot.context_scope
    )
    assert isinstance(
        observation.observation_period,
        RetailCommercialObservationPeriod,
    )


@pytest.mark.parametrize("sold_quantity", [0, 1, 100])
def test_nonnegative_sold_quantity_is_accepted(
    sold_quantity: int,
) -> None:
    observation = create_sales_quantity(
        sold_quantity=sold_quantity,
    )

    assert observation.sold_quantity == sold_quantity


@pytest.mark.parametrize(
    "sold_quantity",
    [True, False, 0.0, "1", None],
)
def test_sold_quantity_requires_strict_integer(
    sold_quantity: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="sold_quantity must be an integer",
    ):
        create_sales_quantity(
            sold_quantity=sold_quantity,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("sold_quantity", [-1, -100])
def test_negative_sold_quantity_is_rejected(
    sold_quantity: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="sold_quantity must not be negative",
    ):
        create_sales_quantity(
            sold_quantity=sold_quantity,
        )


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
            "observation_period",
            "observation_period must be a RetailCommercialObservationPeriod",
        ),
        (
            "quantity_unit",
            "quantity_unit must be a RetailCommercialQuantityUnit",
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
            create_sales_quantity(),
            **{field_name: object()},
        )


@pytest.mark.parametrize("value", ["", " ", "\t", None, 1])
def test_measurement_scheme_id_requires_nonempty_string(
    value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="measurement_scheme_id must not be empty",
    ):
        replace(
            create_sales_quantity(),
            measurement_scheme_id=value,
        )


@pytest.mark.parametrize(
    "value",
    [True, False, 0, -1, 1.0, "1", None],
)
def test_measurement_scheme_version_requires_positive_integer(
    value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "measurement_scheme_version must be a "
            "positive integer"
        ),
    ):
        replace(
            create_sales_quantity(),
            measurement_scheme_version=value,
        )


def test_exact_snapshot_context_scope_reference_is_required() -> None:
    observation = create_sales_quantity()
    foreign_equal_scope = replace(observation.context_scope)

    assert foreign_equal_scope == observation.context_scope
    assert foreign_equal_scope is not observation.context_scope

    with pytest.raises(
        ValueError,
        match="context_scope does not match provenance snapshot",
    ):
        replace(
            observation,
            context_scope=foreign_equal_scope,
        )


def test_snapshot_without_context_scope_is_rejected() -> None:
    context_scope = create_context_scope()

    with pytest.raises(
        ValueError,
        match="context_scope does not match provenance snapshot",
    ):
        RetailProductObservedSalesQuantity(
            product_identity=create_product_identity(),
            context_scope=context_scope,
            observation_period=create_period(),
            sold_quantity=0,
            quantity_unit=RetailCommercialQuantityUnit.UNIT,
            measurement_scheme_id="sales-measurement-001",
            measurement_scheme_version=1,
            provenance_binding=create_binding(
                context_scope=None,
            ),
        )


def test_sales_period_may_end_exactly_at_observed_at() -> None:
    observation = create_sales_quantity()

    assert observation.observation_period.period_until == (
        observation.provenance_binding.provenance.observed_at
    )


def test_sales_period_must_not_end_after_observed_at() -> None:
    context_scope = create_context_scope()
    observed_at = PERIOD_UNTIL - timedelta(microseconds=1)

    with pytest.raises(
        ValueError,
        match="sales period must end no later than observed_at",
    ):
        RetailProductObservedSalesQuantity(
            product_identity=create_product_identity(),
            context_scope=context_scope,
            observation_period=create_period(),
            sold_quantity=0,
            quantity_unit=RetailCommercialQuantityUnit.UNIT,
            measurement_scheme_id="sales-measurement-001",
            measurement_scheme_version=1,
            provenance_binding=create_binding(
                context_scope=context_scope,
                observed_at=observed_at,
            ),
        )


def test_snapshot_and_provenance_identity_are_not_duplicated() -> None:
    field_names = {
        field.name
        for field in fields(RetailProductObservedSalesQuantity)
    }

    assert field_names.isdisjoint(
        {
            "snapshot_id",
            "snapshot_version",
            "case_id",
            "dimension_id",
            "observed_at",
            "evidence_ids",
        }
    )


def test_zero_sales_remains_an_uninterpreted_observation() -> None:
    observation = create_sales_quantity(sold_quantity=0)

    assert observation.sold_quantity == 0
    assert not hasattr(observation, "sales_status")
    assert not hasattr(observation, "commercial_impact")
    assert not hasattr(observation, "availability")


def test_contract_adds_no_sales_basis_or_derived_metric_fields() -> None:
    field_names = {
        field.name
        for field in fields(RetailProductObservedSalesQuantity)
    }

    assert field_names.isdisjoint(
        {
            "gross_sales",
            "net_sales",
            "returns",
            "cancellations",
            "revenue",
            "currency",
            "sell_through",
            "margin",
        }
    )


def test_contract_introduces_no_calculation_recommendation_or_io() -> None:
    module = __import__(
        "sp001.contracts.retail_product_observed_sales_quantity",
        fromlist=["*"],
    )
    source = inspect.getsource(module).lower()

    forbidden = (
        "calculate",
        "formula",
        "recommend",
        "priorit",
        "requests",
        "notion",
        "openai",
        "subprocess",
        "pathlib",
    )

    assert all(term not in source for term in forbidden)
