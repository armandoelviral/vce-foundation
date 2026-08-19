from dataclasses import FrozenInstanceError

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


def create_definition(
    **overrides,
) -> RetailContextDefinition:
    values = {
        "context_definition_id": "CTX-DEFINITION-001",
        "customer_id": "CUSTOMER-PSEUDONYM-001",
        "definition_version": 1,
        "dimension_types": (
            "DEPARTMENT",
            "FIXTURE_TYPE",
            "PRESENTATION_CAPACITY",
        ),
    }

    values.update(
        overrides,
    )

    return RetailContextDefinition(
        **values,
    )


def create_scope(
    **overrides,
) -> RetailContextScope:
    values = {
        "context_id": "CTX-SCOPE-MX-001",
        "commercial_channel_id": "CHANNEL-DEPARTMENT-STORE-MX",
        "point_of_sale_id": "POS-PSEUDONYM-001",
        "department_id": "DEPT-CHILDREN-001",
        "profile_version": 1,
    }

    values.update(
        overrides,
    )

    return RetailContextScope(
        **values,
    )


def create_dimension(
    *,
    dimension_id: str = "CTX-DEPARTMENT-001",
    dimension_type: str = "DEPARTMENT",
) -> RetailContextDimension:
    return RetailContextDimension(
        dimension_id=dimension_id,
        dimension_type=dimension_type,
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CUSTOMER-DECLARED-VALUE",
    )


def create_snapshot(
    **overrides,
) -> RetailContextSnapshot:
    values = {
        "snapshot_id": "RCP-SNAPSHOT-001",
        "snapshot_version": 1,
        "case_id": "CASE-001",
    }

    values.update(
        overrides,
    )

    return RetailContextSnapshot(
        **values,
    )


def test_historical_snapshot_remains_valid_without_definition() -> None:
    snapshot = create_snapshot()

    assert snapshot.context_definition is None


def test_snapshot_preserves_customer_context_definition() -> None:
    definition = create_definition()

    snapshot = create_snapshot(
        context_definition=definition,
    )

    assert snapshot.context_definition is definition


def test_snapshot_preserves_definition_identity() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
    )

    assert (
        snapshot.context_definition.context_definition_id
        == "CTX-DEFINITION-001"
    )


def test_snapshot_preserves_opaque_customer_identity() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
    )

    assert snapshot.context_definition.customer_id == (
        "CUSTOMER-PSEUDONYM-001"
    )


def test_snapshot_preserves_definition_version() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(
            definition_version=3,
        ),
    )

    assert snapshot.context_definition.definition_version == 3


def test_snapshot_preserves_declared_dimension_vocabulary() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
    )

    assert snapshot.context_definition.dimension_types == (
        "DEPARTMENT",
        "FIXTURE_TYPE",
        "PRESENTATION_CAPACITY",
    )


@pytest.mark.parametrize(
    "invalid_definition",
    (
        "CTX-DEFINITION-001",
        1,
        True,
        {},
        [],
    ),
)
def test_snapshot_rejects_invalid_context_definition_type(
    invalid_definition,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "context_definition must be a "
            "RetailContextDefinition"
        ),
    ):
        create_snapshot(
            context_definition=invalid_definition,
        )


def test_snapshot_definition_cannot_be_reassigned() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        snapshot.context_definition = create_definition(
            context_definition_id="CTX-DEFINITION-002",
        )


def test_nested_definition_cannot_be_mutated() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        snapshot.context_definition.customer_id = (
            "CUSTOMER-PSEUDONYM-002"
        )


def test_snapshot_definition_and_scope_coexist() -> None:
    definition = create_definition()

    scope = create_scope()

    snapshot = create_snapshot(
        context_definition=definition,
        context_scope=scope,
    )

    assert snapshot.context_definition is definition
    assert snapshot.context_scope is scope


def test_snapshot_definition_scope_and_dimensions_coexist() -> None:
    definition = create_definition()

    scope = create_scope()

    dimension = create_dimension()

    snapshot = create_snapshot(
        context_definition=definition,
        context_scope=scope,
        dimensions=(
            dimension,
        ),
    )

    assert snapshot.context_definition is definition
    assert snapshot.context_scope is scope

    assert snapshot.dimensions == (
        dimension,
    )


def test_snapshot_definition_version_is_independent() -> None:
    snapshot = create_snapshot(
        snapshot_version=7,
        context_definition=create_definition(
            definition_version=3,
        ),
        context_scope=create_scope(
            profile_version=5,
        ),
    )

    assert snapshot.snapshot_version == 7

    assert snapshot.context_definition.definition_version == 3

    assert snapshot.context_scope.profile_version == 5


def test_same_definition_can_support_distinct_store_scopes() -> None:
    definition = create_definition()

    first = create_snapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        context_definition=definition,
        context_scope=create_scope(
            context_id="CTX-SCOPE-MX-001",
            point_of_sale_id="POS-PSEUDONYM-001",
        ),
    )

    second = create_snapshot(
        snapshot_id="RCP-SNAPSHOT-002",
        context_definition=definition,
        context_scope=create_scope(
            context_id="CTX-SCOPE-MX-002",
            point_of_sale_id="POS-PSEUDONYM-002",
        ),
    )

    assert first.context_definition == (
        second.context_definition
    )

    assert first.context_scope.point_of_sale_id != (
        second.context_scope.point_of_sale_id
    )


def test_same_scope_can_use_new_definition_version() -> None:
    scope = create_scope()

    first = create_snapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        context_scope=scope,
        context_definition=create_definition(
            definition_version=1,
            dimension_types=(
                "DEPARTMENT",
            ),
        ),
    )

    second = create_snapshot(
        snapshot_id="RCP-SNAPSHOT-002",
        snapshot_version=2,
        context_scope=scope,
        context_definition=create_definition(
            definition_version=2,
            dimension_types=(
                "DEPARTMENT",
                "PURCHASE_VOLUME",
            ),
        ),
    )

    assert first.context_scope == second.context_scope

    assert (
        first.context_definition.definition_version
        == 1
    )

    assert (
        second.context_definition.definition_version
        == 2
    )


def test_distinct_customers_remain_distinct_definitions() -> None:
    first = create_snapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        context_definition=create_definition(
            context_definition_id="CTX-DEFINITION-001",
            customer_id="CUSTOMER-PSEUDONYM-001",
        ),
    )

    second = create_snapshot(
        snapshot_id="RCP-SNAPSHOT-002",
        context_definition=create_definition(
            context_definition_id="CTX-DEFINITION-002",
            customer_id="CUSTOMER-PSEUDONYM-002",
        ),
    )

    assert (
        first.context_definition.customer_id
        != second.context_definition.customer_id
    )

    assert (
        first.context_definition.context_definition_id
        != second.context_definition.context_definition_id
    )


def test_definition_does_not_synthesize_missing_dimensions() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(
            dimension_types=(
                "DEPARTMENT",
                "PRESENTATION_CAPACITY",
            ),
        ),
        dimensions=(),
    )

    assert snapshot.dimensions == ()

    assert snapshot.context_definition.dimension_types == (
        "DEPARTMENT",
        "PRESENTATION_CAPACITY",
    )


def test_definition_does_not_replace_case_identity() -> None:
    snapshot = create_snapshot(
        case_id="CASE-RETAIL-001",
        context_definition=create_definition(),
    )

    assert snapshot.case_id == "CASE-RETAIL-001"

    assert (
        snapshot.context_definition.context_definition_id
        == "CTX-DEFINITION-001"
    )


def test_definition_does_not_infer_scope_authority_or_ownership() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
    )

    assert snapshot.context_scope is None

    assert not hasattr(
        snapshot.context_definition,
        "authority",
    )

    assert not hasattr(
        snapshot.context_definition,
        "owner",
    )
