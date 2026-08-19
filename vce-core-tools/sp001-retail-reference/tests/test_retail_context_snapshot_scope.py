from dataclasses import FrozenInstanceError

import pytest

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


def create_dimension() -> RetailContextDimension:
    return RetailContextDimension(
        dimension_id="CTX-FIXTURE-001",
        dimension_type="FIXTURE_TYPE",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CUSTOMER-DECLARED-FIXTURE",
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


def test_historical_snapshot_remains_valid_without_scope() -> None:
    snapshot = create_snapshot()

    assert snapshot.context_scope is None


def test_snapshot_preserves_declared_context_scope() -> None:
    scope = create_scope()

    snapshot = create_snapshot(
        context_scope=scope,
    )

    assert snapshot.context_scope is scope


def test_snapshot_preserves_context_identity() -> None:
    snapshot = create_snapshot(
        context_scope=create_scope(),
    )

    assert snapshot.context_scope.context_id == (
        "CTX-SCOPE-MX-001"
    )


def test_snapshot_preserves_commercial_channel_identity() -> None:
    snapshot = create_snapshot(
        context_scope=create_scope(),
    )

    assert snapshot.context_scope.commercial_channel_id == (
        "CHANNEL-DEPARTMENT-STORE-MX"
    )


def test_snapshot_preserves_pseudonymized_point_of_sale() -> None:
    snapshot = create_snapshot(
        context_scope=create_scope(),
    )

    assert snapshot.context_scope.point_of_sale_id == (
        "POS-PSEUDONYM-001"
    )


def test_snapshot_preserves_department_identity() -> None:
    snapshot = create_snapshot(
        context_scope=create_scope(),
    )

    assert snapshot.context_scope.department_id == (
        "DEPT-CHILDREN-001"
    )


def test_snapshot_preserves_profile_version() -> None:
    snapshot = create_snapshot(
        context_scope=create_scope(
            profile_version=2,
        ),
    )

    assert snapshot.context_scope.profile_version == 2


def test_snapshot_and_profile_versions_remain_independent() -> None:
    snapshot = create_snapshot(
        snapshot_version=3,
        context_scope=create_scope(
            profile_version=7,
        ),
    )

    assert snapshot.snapshot_version == 3
    assert snapshot.context_scope.profile_version == 7


@pytest.mark.parametrize(
    "invalid_scope",
    (
        "CTX-SCOPE-MX-001",
        1,
        True,
        {},
        [],
    ),
)
def test_snapshot_rejects_invalid_context_scope_type(
    invalid_scope,
) -> None:
    with pytest.raises(
        TypeError,
        match="context_scope must be a RetailContextScope",
    ):
        create_snapshot(
            context_scope=invalid_scope,
        )


def test_snapshot_scope_cannot_be_reassigned() -> None:
    snapshot = create_snapshot(
        context_scope=create_scope(),
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        snapshot.context_scope = create_scope(
            context_id="CTX-SCOPE-MX-002",
            point_of_sale_id="POS-PSEUDONYM-002",
        )


def test_snapshot_nested_scope_cannot_be_mutated() -> None:
    snapshot = create_snapshot(
        context_scope=create_scope(),
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        snapshot.context_scope.point_of_sale_id = (
            "POS-PSEUDONYM-002"
        )


def test_snapshot_preserves_scope_and_dimensions_together() -> None:
    scope = create_scope()

    dimension = create_dimension()

    snapshot = create_snapshot(
        dimensions=(
            dimension,
        ),
        context_scope=scope,
    )

    assert snapshot.context_scope is scope

    assert snapshot.dimensions == (
        dimension,
    )


def test_same_case_can_preserve_distinct_store_contexts() -> None:
    first = create_snapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        context_scope=create_scope(
            context_id="CTX-SCOPE-MX-001",
            point_of_sale_id="POS-PSEUDONYM-001",
        ),
    )

    second = create_snapshot(
        snapshot_id="RCP-SNAPSHOT-002",
        context_scope=create_scope(
            context_id="CTX-SCOPE-MX-002",
            point_of_sale_id="POS-PSEUDONYM-002",
        ),
    )

    assert first.case_id == second.case_id

    assert first.context_scope.commercial_channel_id == (
        second.context_scope.commercial_channel_id
    )

    assert first.context_scope.department_id == (
        second.context_scope.department_id
    )

    assert first.context_scope.point_of_sale_id != (
        second.context_scope.point_of_sale_id
    )


def test_same_store_can_preserve_distinct_departments() -> None:
    first = create_snapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        context_scope=create_scope(
            context_id="CTX-SCOPE-MX-001",
            department_id="DEPT-GIRLS-001",
        ),
    )

    second = create_snapshot(
        snapshot_id="RCP-SNAPSHOT-002",
        context_scope=create_scope(
            context_id="CTX-SCOPE-MX-002",
            department_id="DEPT-BOYS-001",
        ),
    )

    assert first.context_scope.point_of_sale_id == (
        second.context_scope.point_of_sale_id
    )

    assert first.context_scope.department_id != (
        second.context_scope.department_id
    )


def test_snapshot_version_change_preserves_prior_scope() -> None:
    original_scope = create_scope(
        profile_version=1,
    )

    updated_scope = create_scope(
        profile_version=2,
    )

    first = create_snapshot(
        snapshot_version=1,
        context_scope=original_scope,
    )

    second = create_snapshot(
        snapshot_version=2,
        context_scope=updated_scope,
    )

    assert first.snapshot_version == 1
    assert first.context_scope.profile_version == 1

    assert second.snapshot_version == 2
    assert second.context_scope.profile_version == 2


def test_scope_does_not_replace_existing_case_identity() -> None:
    snapshot = create_snapshot(
        case_id="CASE-RETAIL-001",
        context_scope=create_scope(),
    )

    assert snapshot.case_id == (
        "CASE-RETAIL-001"
    )

    assert snapshot.context_scope.context_id == (
        "CTX-SCOPE-MX-001"
    )


def test_snapshot_does_not_infer_fixture_count_from_scope() -> None:
    snapshot = create_snapshot(
        context_scope=create_scope(),
    )

    assert snapshot.dimensions == ()

    assert not hasattr(
        snapshot.context_scope,
        "fixture_count",
    )


def test_snapshot_does_not_infer_authority_from_scope() -> None:
    snapshot = create_snapshot(
        context_scope=create_scope(),
    )

    assert not hasattr(
        snapshot.context_scope,
        "authority",
    )

    assert not hasattr(
        snapshot.context_scope,
        "owner",
    )
