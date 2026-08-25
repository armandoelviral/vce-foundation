from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.contracts.retail_context_definition import (
    RetailContextDefinition,
)
from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)
from sp001.contracts.retail_context_scope import (
    RetailContextScope,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)
from sp001.contracts.retail_expected_state import (
    RetailExpectedState,
)


def create_scope(
    *,
    context_id: str = "CONTEXT-STORE-A",
    point_of_sale_id: str = "STORE-A",
) -> RetailContextScope:
    return RetailContextScope(
        context_id=context_id,
        commercial_channel_id="DEPARTMENT_STORE",
        point_of_sale_id=point_of_sale_id,
        department_id="GIRLS",
        profile_version=1,
    )


def create_definition(
    *,
    context_definition_id: str = "DEFINITION-CUSTOMER-A",
    customer_id: str = "CUSTOMER-A",
) -> RetailContextDefinition:
    return RetailContextDefinition(
        context_definition_id=context_definition_id,
        customer_id=customer_id,
        definition_version=1,
        dimension_types=(
            "DEPARTMENT",
            "INVENTORY_STATE",
        ),
        required_dimension_types=(
            "DEPARTMENT",
            "INVENTORY_STATE",
        ),
        optional_dimension_types=(),
    )


def create_dimensions() -> tuple[
    RetailContextDimension,
    ...,
]:
    return (
        RetailContextDimension(
            dimension_id="DIM-DEPARTMENT-001",
            dimension_type="DEPARTMENT",
            applicability=DimensionApplicability.REQUIRED,
            evidence_status=DimensionEvidenceStatus.DOCUMENTED,
            value="GIRLS",
        ),
        RetailContextDimension(
            dimension_id="DIM-INVENTORY-001",
            dimension_type="INVENTORY_STATE",
            applicability=DimensionApplicability.REQUIRED,
            evidence_status=DimensionEvidenceStatus.DOCUMENTED,
            value="AVAILABLE",
        ),
    )


def create_snapshot(
    *,
    snapshot_id: str = "SNAPSHOT-STORE-A",
    case_id: str = "CASE-STORE-A",
    context_scope: RetailContextScope | None = None,
    context_definition: RetailContextDefinition | None = None,
    include_scope: bool = True,
    include_definition: bool = True,
) -> RetailContextSnapshot:
    scope = (
        context_scope or create_scope()
        if include_scope
        else None
    )

    definition = (
        context_definition or create_definition()
        if include_definition
        else None
    )

    return RetailContextSnapshot(
        snapshot_id=snapshot_id,
        snapshot_version=1,
        case_id=case_id,
        context_scope=scope,
        context_definition=definition,
        dimensions=create_dimensions(),
    )


def create_expected_state(
    *,
    expected_state_id: str = "EXPECTED-STATE-001",
    expected_state_version: int = 1,
    snapshot: RetailContextSnapshot | None = None,
    expectation_type: str = "VISIBILITY_PRIORITY",
    expected_value: str = "HERO",
    source_dimension_ids: tuple[str, ...] = (
        "DIM-DEPARTMENT-001",
        "DIM-INVENTORY-001",
    ),
    source_policy_ids: tuple[str, ...] = (
        "CP01-CONTEXTUAL-ADAPTATION",
    ),
) -> RetailExpectedState:
    return RetailExpectedState(
        expected_state_id=expected_state_id,
        expected_state_version=expected_state_version,
        snapshot=(
            snapshot
            if snapshot is not None
            else create_snapshot()
        ),
        expectation_type=expectation_type,
        expected_value=expected_value,
        source_dimension_ids=source_dimension_ids,
        source_policy_ids=source_policy_ids,
    )


def test_expected_state_has_exact_minimal_contract() -> None:
    assert tuple(
        field.name
        for field in fields(
            RetailExpectedState,
        )
    ) == (
        "expected_state_id",
        "expected_state_version",
        "snapshot",
        "expectation_type",
        "expected_value",
        "source_dimension_ids",
        "source_policy_ids",
    )


def test_expected_state_preserves_explicit_identity() -> None:
    state = create_expected_state()

    assert state.expected_state_id == (
        "EXPECTED-STATE-001"
    )
    assert state.expected_state_version == 1


@pytest.mark.parametrize(
    "invalid_identity",
    (
        "",
        "   ",
        None,
        7,
    ),
)
def test_expected_state_rejects_invalid_identity(
    invalid_identity: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="expected_state_id must not be empty",
    ):
        create_expected_state(
            expected_state_id=invalid_identity,
        )


@pytest.mark.parametrize(
    "invalid_version",
    (
        0,
        -1,
        True,
        False,
        1.5,
        "1",
    ),
)
def test_expected_state_requires_positive_integer_version(
    invalid_version: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "expected_state_version must be "
            "a positive integer"
        ),
    ):
        create_expected_state(
            expected_state_version=invalid_version,
        )


def test_expected_state_preserves_snapshot_identity() -> None:
    snapshot = create_snapshot()

    state = create_expected_state(
        snapshot=snapshot,
    )

    assert state.snapshot is snapshot
    assert state.snapshot.snapshot_id == (
        "SNAPSHOT-STORE-A"
    )
    assert state.snapshot.case_id == (
        "CASE-STORE-A"
    )


def test_expected_state_preserves_operating_store_identity() -> None:
    state = create_expected_state()

    assert state.snapshot.context_scope.context_id == (
        "CONTEXT-STORE-A"
    )
    assert state.snapshot.context_scope.point_of_sale_id == (
        "STORE-A"
    )


def test_expected_state_preserves_customer_definition_identity() -> None:
    state = create_expected_state()

    assert state.snapshot.context_definition.customer_id == (
        "CUSTOMER-A"
    )
    assert (
        state.snapshot.context_definition
        .context_definition_id
    ) == (
        "DEFINITION-CUSTOMER-A"
    )


def test_expected_state_rejects_invalid_snapshot() -> None:
    with pytest.raises(
        TypeError,
        match="snapshot must be a RetailContextSnapshot",
    ):
        RetailExpectedState(
            expected_state_id="EXPECTED-STATE-001",
            expected_state_version=1,
            snapshot=None,
            expectation_type="VISIBILITY_PRIORITY",
            expected_value="HERO",
            source_dimension_ids=(
                "DIM-DEPARTMENT-001",
            ),
        )


def test_expected_state_requires_explicit_operating_scope() -> None:
    snapshot = create_snapshot(
        include_scope=False,
    )

    with pytest.raises(
        ValueError,
        match="expected state requires context_scope",
    ):
        create_expected_state(
            snapshot=snapshot,
        )


def test_expected_state_requires_explicit_customer_definition() -> None:
    snapshot = create_snapshot(
        include_definition=False,
    )

    with pytest.raises(
        ValueError,
        match="expected state requires context_definition",
    ):
        create_expected_state(
            snapshot=snapshot,
        )


def test_expected_state_preserves_open_customer_expectation_type() -> None:
    state = create_expected_state(
        expectation_type="CUSTOMER_DEFINED_LOCAL_PRIORITY",
        expected_value="WINDOW_FACING",
    )

    assert state.expectation_type == (
        "CUSTOMER_DEFINED_LOCAL_PRIORITY"
    )
    assert state.expected_value == (
        "WINDOW_FACING"
    )


@pytest.mark.parametrize(
    "invalid_expectation_type",
    (
        "",
        "   ",
        None,
        7,
    ),
)
def test_expected_state_rejects_invalid_expectation_type(
    invalid_expectation_type: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="expectation_type must not be empty",
    ):
        create_expected_state(
            expectation_type=invalid_expectation_type,
        )


@pytest.mark.parametrize(
    "invalid_expected_value",
    (
        "",
        "   ",
        None,
        7,
    ),
)
def test_expected_state_requires_explicit_expected_value(
    invalid_expected_value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="expected_value must not be empty",
    ):
        create_expected_state(
            expected_value=invalid_expected_value,
        )


def test_expected_state_preserves_declared_source_dimensions() -> None:
    state = create_expected_state()

    assert state.source_dimension_ids == (
        "DIM-DEPARTMENT-001",
        "DIM-INVENTORY-001",
    )


def test_expected_state_rejects_mutable_source_dimensions() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "source_dimension_ids must be "
            "an immutable tuple"
        ),
    ):
        create_expected_state(
            source_dimension_ids=[
                "DIM-DEPARTMENT-001",
            ],
        )


def test_expected_state_requires_at_least_one_source_dimension() -> None:
    with pytest.raises(
        ValueError,
        match="source_dimension_ids must not be empty",
    ):
        create_expected_state(
            source_dimension_ids=(),
        )


@pytest.mark.parametrize(
    "invalid_dimension_id",
    (
        "",
        "   ",
        None,
        7,
    ),
)
def test_expected_state_rejects_invalid_source_dimension_identity(
    invalid_dimension_id: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="source dimension_id must not be empty",
    ):
        create_expected_state(
            source_dimension_ids=(
                invalid_dimension_id,
            ),
        )


def test_expected_state_rejects_duplicate_source_dimension() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "duplicate source dimension_id: "
            "DIM-DEPARTMENT-001"
        ),
    ):
        create_expected_state(
            source_dimension_ids=(
                "DIM-DEPARTMENT-001",
                "DIM-DEPARTMENT-001",
            ),
        )


def test_expected_state_rejects_dimension_absent_from_snapshot() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "source dimension_id not present in snapshot: "
            "DIM-UNKNOWN"
        ),
    ):
        create_expected_state(
            source_dimension_ids=(
                "DIM-UNKNOWN",
            ),
        )


def test_expected_state_preserves_explicit_policy_reference() -> None:
    state = create_expected_state()

    assert state.source_policy_ids == (
        "CP01-CONTEXTUAL-ADAPTATION",
    )


def test_expected_state_allows_no_policy_when_none_is_declared() -> None:
    state = create_expected_state(
        source_policy_ids=(),
    )

    assert state.source_policy_ids == ()


def test_expected_state_rejects_mutable_policy_references() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "source_policy_ids must be "
            "an immutable tuple"
        ),
    ):
        create_expected_state(
            source_policy_ids=[
                "CP01-CONTEXTUAL-ADAPTATION",
            ],
        )


@pytest.mark.parametrize(
    "invalid_policy_id",
    (
        "",
        "   ",
        None,
        7,
    ),
)
def test_expected_state_rejects_invalid_policy_reference(
    invalid_policy_id: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="source policy_id must not be empty",
    ):
        create_expected_state(
            source_policy_ids=(
                invalid_policy_id,
            ),
        )


def test_expected_state_rejects_duplicate_policy_reference() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "duplicate source policy_id: "
            "CP01-CONTEXTUAL-ADAPTATION"
        ),
    ):
        create_expected_state(
            source_policy_ids=(
                "CP01-CONTEXTUAL-ADAPTATION",
                "CP01-CONTEXTUAL-ADAPTATION",
            ),
        )


def test_expected_state_preserves_source_dimension_order() -> None:
    state = create_expected_state(
        source_dimension_ids=(
            "DIM-INVENTORY-001",
            "DIM-DEPARTMENT-001",
        ),
    )

    assert state.source_dimension_ids == (
        "DIM-INVENTORY-001",
        "DIM-DEPARTMENT-001",
    )


def test_expected_state_is_immutable() -> None:
    state = create_expected_state()

    with pytest.raises(
        FrozenInstanceError,
    ):
        state.expected_value = "SUPPORT"


def test_distinct_store_contexts_can_preserve_distinct_expected_values() -> None:
    snapshot_a = create_snapshot()

    snapshot_b = create_snapshot(
        snapshot_id="SNAPSHOT-STORE-B",
        case_id="CASE-STORE-B",
        context_scope=create_scope(
            context_id="CONTEXT-STORE-B",
            point_of_sale_id="STORE-B",
        ),
        context_definition=create_definition(
            context_definition_id="DEFINITION-CUSTOMER-B",
            customer_id="CUSTOMER-B",
        ),
    )

    state_a = create_expected_state(
        expected_state_id="EXPECTED-STATE-A",
        snapshot=snapshot_a,
        expectation_type="VISIBILITY_PRIORITY",
        expected_value="HERO",
    )

    state_b = create_expected_state(
        expected_state_id="EXPECTED-STATE-B",
        snapshot=snapshot_b,
        expectation_type="VISIBILITY_PRIORITY",
        expected_value="SUPPORT",
    )

    assert state_a.expectation_type == (
        state_b.expectation_type
    )
    assert state_a.expected_value != (
        state_b.expected_value
    )
    assert (
        state_a.snapshot.context_scope.point_of_sale_id
        != state_b.snapshot.context_scope.point_of_sale_id
    )


def test_expected_state_does_not_infer_inventory_fixture_or_authority() -> None:
    state = create_expected_state()

    for attribute in (
        "sku_id",
        "fixture_id",
        "fixture_slot_id",
        "facing_count",
        "commercial_impact_status",
        "customer_acceptance_status",
        "authority",
        "owner",
        "valid_from",
        "valid_until",
    ):
        assert not hasattr(
            state,
            attribute,
        )
