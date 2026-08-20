import pytest

from sp001.contracts.retail_context_definition import (
    RetailContextDefinition,
)
from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)


def create_definition(
    *dimension_types: str,
    customer_id: str = "CUSTOMER-PSEUDONYM-001",
    definition_version: int = 1,
) -> RetailContextDefinition:
    return RetailContextDefinition(
        context_definition_id="CTX-DEFINITION-001",
        customer_id=customer_id,
        definition_version=definition_version,
        dimension_types=dimension_types,
    )


def create_dimension(
    *,
    dimension_id: str,
    dimension_type: str,
    applicability: DimensionApplicability = (
        DimensionApplicability.REQUIRED
    ),
    evidence_status: DimensionEvidenceStatus = (
        DimensionEvidenceStatus.DOCUMENTED
    ),
    value: str | None = "CUSTOMER-DECLARED-VALUE",
) -> RetailContextDimension:
    return RetailContextDimension(
        dimension_id=dimension_id,
        dimension_type=dimension_type,
        applicability=applicability,
        evidence_status=evidence_status,
        value=value,
    )


def create_snapshot(
    *,
    dimensions: tuple[RetailContextDimension, ...] = (),
    definition: RetailContextDefinition | None = None,
) -> RetailContextSnapshot:
    return RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
        dimensions=dimensions,
        context_definition=definition,
    )


def test_historical_snapshot_accepts_dimensions_without_definition() -> None:
    dimension = create_dimension(
        dimension_id="CTX-LEGACY-001",
        dimension_type="LEGACY_CUSTOMER_DIMENSION",
    )

    snapshot = create_snapshot(
        dimensions=(
            dimension,
        ),
    )

    assert snapshot.context_definition is None

    assert snapshot.dimensions == (
        dimension,
    )


def test_snapshot_accepts_one_declared_dimension_type() -> None:
    definition = create_definition(
        "DEPARTMENT",
    )

    dimension = create_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
    )

    snapshot = create_snapshot(
        dimensions=(
            dimension,
        ),
        definition=definition,
    )

    assert snapshot.dimensions == (
        dimension,
    )


def test_snapshot_accepts_multiple_declared_dimension_types() -> None:
    definition = create_definition(
        "DEPARTMENT",
        "FIXTURE_TYPE",
        "PRESENTATION_CAPACITY",
    )

    dimensions = (
        create_dimension(
            dimension_id="CTX-DEPARTMENT-001",
            dimension_type="DEPARTMENT",
        ),
        create_dimension(
            dimension_id="CTX-FIXTURE-001",
            dimension_type="FIXTURE_TYPE",
        ),
        create_dimension(
            dimension_id="CTX-CAPACITY-001",
            dimension_type="PRESENTATION_CAPACITY",
        ),
    )

    snapshot = create_snapshot(
        dimensions=dimensions,
        definition=definition,
    )

    assert snapshot.dimensions == dimensions


def test_snapshot_rejects_undeclared_dimension_type() -> None:
    definition = create_definition(
        "DEPARTMENT",
    )

    dimension = create_dimension(
        dimension_id="CTX-INVENTORY-001",
        dimension_type="INVENTORY_STATE",
    )

    with pytest.raises(
        ValueError,
        match="undeclared dimension_type: INVENTORY_STATE",
    ):
        create_snapshot(
            dimensions=(
                dimension,
            ),
            definition=definition,
        )


def test_snapshot_rejects_undeclared_type_after_valid_dimension() -> None:
    definition = create_definition(
        "DEPARTMENT",
    )

    declared = create_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
    )

    undeclared = create_dimension(
        dimension_id="CTX-INVENTORY-001",
        dimension_type="INVENTORY_STATE",
    )

    with pytest.raises(
        ValueError,
        match="undeclared dimension_type: INVENTORY_STATE",
    ):
        create_snapshot(
            dimensions=(
                declared,
                undeclared,
            ),
            definition=definition,
        )


@pytest.mark.parametrize(
    "dimension_type",
    (
        "FLOOR_AREA",
        "FIXTURE_TYPE",
        "PURCHASE_VOLUME",
        "COMMERCIAL_CLUSTER",
        "CUSTOMER_DEFINED_LOCAL_REQUIREMENT",
    ),
)
def test_snapshot_rejects_any_type_absent_from_customer_definition(
    dimension_type: str,
) -> None:
    definition = create_definition(
        "DEPARTMENT",
    )

    dimension = create_dimension(
        dimension_id="CTX-UNDECLARED-001",
        dimension_type=dimension_type,
    )

    with pytest.raises(
        ValueError,
        match=f"undeclared dimension_type: {dimension_type}",
    ):
        create_snapshot(
            dimensions=(
                dimension,
            ),
            definition=definition,
        )


def test_customer_defined_dimension_type_remains_supported() -> None:
    definition = create_definition(
        "CUSTOMER_DEFINED_COMMERCIAL_ZONE",
    )

    dimension = create_dimension(
        dimension_id="CTX-CUSTOM-001",
        dimension_type="CUSTOMER_DEFINED_COMMERCIAL_ZONE",
    )

    snapshot = create_snapshot(
        dimensions=(
            dimension,
        ),
        definition=definition,
    )

    assert snapshot.dimensions[0].dimension_type == (
        "CUSTOMER_DEFINED_COMMERCIAL_ZONE"
    )


def test_declared_but_absent_dimensions_remain_unsynthesized() -> None:
    definition = create_definition(
        "DEPARTMENT",
        "PRESENTATION_CAPACITY",
    )

    snapshot = create_snapshot(
        dimensions=(),
        definition=definition,
    )

    assert snapshot.dimensions == ()

    assert snapshot.context_definition.dimension_types == (
        "DEPARTMENT",
        "PRESENTATION_CAPACITY",
    )


def test_partially_present_declared_dimensions_remain_valid() -> None:
    definition = create_definition(
        "DEPARTMENT",
        "PRESENTATION_CAPACITY",
    )

    department = create_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
    )

    snapshot = create_snapshot(
        dimensions=(
            department,
        ),
        definition=definition,
    )

    assert len(
        snapshot.dimensions,
    ) == 1

    assert snapshot.dimensions[0].dimension_type == (
        "DEPARTMENT"
    )


def test_multiple_dimensions_of_same_declared_type_remain_valid() -> None:
    definition = create_definition(
        "ACTIVE_CATEGORY",
    )

    first = create_dimension(
        dimension_id="CTX-CATEGORY-001",
        dimension_type="ACTIVE_CATEGORY",
        value="TODDLER_BOYS",
    )

    second = create_dimension(
        dimension_id="CTX-CATEGORY-002",
        dimension_type="ACTIVE_CATEGORY",
        value="TODDLER_GIRLS",
    )

    snapshot = create_snapshot(
        dimensions=(
            first,
            second,
        ),
        definition=definition,
    )

    assert len(
        snapshot.dimensions,
    ) == 2


def test_declared_optional_dimension_remains_valid() -> None:
    definition = create_definition(
        "PRESENTATION_CAPACITY",
    )

    dimension = create_dimension(
        dimension_id="CTX-CAPACITY-001",
        dimension_type="PRESENTATION_CAPACITY",
        applicability=DimensionApplicability.OPTIONAL,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
        value=None,
    )

    snapshot = create_snapshot(
        dimensions=(
            dimension,
        ),
        definition=definition,
    )

    assert snapshot.dimensions[0].value is None

    assert (
        snapshot.dimensions[0].applicability
        is DimensionApplicability.OPTIONAL
    )


def test_declared_not_applicable_dimension_remains_valid() -> None:
    definition = create_definition(
        "PRESENTATION_CAPACITY",
    )

    dimension = create_dimension(
        dimension_id="CTX-CAPACITY-001",
        dimension_type="PRESENTATION_CAPACITY",
        applicability=DimensionApplicability.NOT_APPLICABLE,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
        value=None,
    )

    snapshot = create_snapshot(
        dimensions=(
            dimension,
        ),
        definition=definition,
    )

    assert (
        snapshot.dimensions[0].applicability
        is DimensionApplicability.NOT_APPLICABLE
    )


def test_declared_disputed_dimension_preserves_uncertainty() -> None:
    definition = create_definition(
        "RETAILER_CONTEXT",
    )

    dimension = create_dimension(
        dimension_id="CTX-RETAILER-001",
        dimension_type="RETAILER_CONTEXT",
        applicability=DimensionApplicability.DISPUTED,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value="SEARS_MEXICO_HUMAN_DECLARED",
    )

    snapshot = create_snapshot(
        dimensions=(
            dimension,
        ),
        definition=definition,
    )

    assert (
        snapshot.dimensions[0].applicability
        is DimensionApplicability.DISPUTED
    )

    assert (
        snapshot.dimensions[0].evidence_status
        is DimensionEvidenceStatus.DISPUTED
    )


def test_distinct_customers_can_authorize_distinct_dimension_types() -> None:
    first_definition = create_definition(
        "DEPARTMENT",
        customer_id="CUSTOMER-PSEUDONYM-001",
    )

    second_definition = create_definition(
        "COMMERCIAL_CLUSTER",
        customer_id="CUSTOMER-PSEUDONYM-002",
    )

    first_dimension = create_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
    )

    second_dimension = create_dimension(
        dimension_id="CTX-CLUSTER-001",
        dimension_type="COMMERCIAL_CLUSTER",
    )

    first = create_snapshot(
        dimensions=(
            first_dimension,
        ),
        definition=first_definition,
    )

    second = create_snapshot(
        dimensions=(
            second_dimension,
        ),
        definition=second_definition,
    )

    assert (
        first.context_definition.customer_id
        != second.context_definition.customer_id
    )

    assert (
        first.dimensions[0].dimension_type
        != second.dimensions[0].dimension_type
    )


def test_new_definition_version_can_authorize_new_dimension_type() -> None:
    previous = create_definition(
        "DEPARTMENT",
        definition_version=1,
    )

    current = create_definition(
        "DEPARTMENT",
        "PURCHASE_VOLUME",
        definition_version=2,
    )

    volume = create_dimension(
        dimension_id="CTX-VOLUME-001",
        dimension_type="PURCHASE_VOLUME",
    )

    with pytest.raises(
        ValueError,
        match="undeclared dimension_type: PURCHASE_VOLUME",
    ):
        create_snapshot(
            dimensions=(
                volume,
            ),
            definition=previous,
        )

    snapshot = create_snapshot(
        dimensions=(
            volume,
        ),
        definition=current,
    )

    assert snapshot.context_definition.definition_version == 2


def test_dimension_type_matching_is_case_sensitive() -> None:
    definition = create_definition(
        "DEPARTMENT",
    )

    dimension = create_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        dimension_type="department",
    )

    with pytest.raises(
        ValueError,
        match="undeclared dimension_type: department",
    ):
        create_snapshot(
            dimensions=(
                dimension,
            ),
            definition=definition,
        )


def test_definition_matching_preserves_dimension_order() -> None:
    definition = create_definition(
        "DEPARTMENT",
        "FIXTURE_TYPE",
    )

    fixture = create_dimension(
        dimension_id="CTX-FIXTURE-001",
        dimension_type="FIXTURE_TYPE",
    )

    department = create_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
    )

    snapshot = create_snapshot(
        dimensions=(
            fixture,
            department,
        ),
        definition=definition,
    )

    assert snapshot.dimensions == (
        fixture,
        department,
    )


def test_definition_matching_does_not_infer_fixture_counts() -> None:
    definition = create_definition(
        "ACTIVE_CATEGORY",
    )

    dimensions = (
        create_dimension(
            dimension_id="CTX-CATEGORY-001",
            dimension_type="ACTIVE_CATEGORY",
            value="TODDLER_BOYS",
        ),
        create_dimension(
            dimension_id="CTX-CATEGORY-002",
            dimension_type="ACTIVE_CATEGORY",
            value="TODDLER_GIRLS",
        ),
    )

    snapshot = create_snapshot(
        dimensions=dimensions,
        definition=definition,
    )

    assert len(
        snapshot.dimensions,
    ) == 2

    assert not hasattr(
        snapshot,
        "fixture_count",
    )
