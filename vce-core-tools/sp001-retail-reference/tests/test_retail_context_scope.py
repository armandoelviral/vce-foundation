from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.retail_context_scope import (
    RetailContextScope,
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


def test_scope_preserves_explicit_context_identity() -> None:
    scope = create_scope()

    assert scope.context_id == (
        "CTX-SCOPE-MX-001"
    )


def test_scope_preserves_declared_commercial_channel() -> None:
    scope = create_scope()

    assert scope.commercial_channel_id == (
        "CHANNEL-DEPARTMENT-STORE-MX"
    )


def test_scope_preserves_pseudonymized_point_of_sale() -> None:
    scope = create_scope()

    assert scope.point_of_sale_id == (
        "POS-PSEUDONYM-001"
    )


def test_scope_preserves_explicit_department_identity() -> None:
    scope = create_scope()

    assert scope.department_id == (
        "DEPT-CHILDREN-001"
    )


def test_scope_preserves_explicit_profile_version() -> None:
    scope = create_scope()

    assert scope.profile_version == 1


@pytest.mark.parametrize(
    "field",
    (
        "context_id",
        "commercial_channel_id",
        "point_of_sale_id",
        "department_id",
    ),
)
def test_scope_rejects_empty_identity(
    field: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        create_scope(
            **{
                field: "",
            }
        )


@pytest.mark.parametrize(
    "field",
    (
        "context_id",
        "commercial_channel_id",
        "point_of_sale_id",
        "department_id",
    ),
)
def test_scope_rejects_blank_identity(
    field: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        create_scope(
            **{
                field: "   ",
            }
        )


@pytest.mark.parametrize(
    "field",
    (
        "context_id",
        "commercial_channel_id",
        "point_of_sale_id",
        "department_id",
    ),
)
def test_scope_rejects_non_string_identity(
    field: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        create_scope(
            **{
                field: 123,
            }
        )


@pytest.mark.parametrize(
    "version",
    (
        0,
        -1,
        True,
        False,
        "1",
        None,
    ),
)
def test_scope_rejects_invalid_profile_version(
    version,
) -> None:
    with pytest.raises(
        ValueError,
        match="profile_version must be a positive integer",
    ):
        create_scope(
            profile_version=version,
        )


def test_scope_is_immutable() -> None:
    scope = create_scope()

    with pytest.raises(
        FrozenInstanceError,
    ):
        scope.point_of_sale_id = (
            "POS-PSEUDONYM-002"
        )


def test_distinct_points_of_sale_remain_distinct_contexts() -> None:
    first = create_scope(
        context_id="CTX-SCOPE-MX-001",
        point_of_sale_id="POS-PSEUDONYM-001",
    )

    second = create_scope(
        context_id="CTX-SCOPE-MX-002",
        point_of_sale_id="POS-PSEUDONYM-002",
    )

    assert first.commercial_channel_id == (
        second.commercial_channel_id
    )

    assert first.department_id == (
        second.department_id
    )

    assert first.point_of_sale_id != (
        second.point_of_sale_id
    )

    assert first != second


def test_distinct_departments_remain_distinct_contexts() -> None:
    first = create_scope(
        context_id="CTX-SCOPE-MX-001",
        department_id="DEPT-GIRLS-001",
    )

    second = create_scope(
        context_id="CTX-SCOPE-MX-002",
        department_id="DEPT-BOYS-001",
    )

    assert first.point_of_sale_id == (
        second.point_of_sale_id
    )

    assert first.department_id != (
        second.department_id
    )

    assert first != second


def test_distinct_profile_versions_remain_distinct_contexts() -> None:
    first = create_scope(
        profile_version=1,
    )

    second = create_scope(
        profile_version=2,
    )

    assert first.context_id == (
        second.context_id
    )

    assert first.profile_version == 1
    assert second.profile_version == 2
    assert first != second


def test_scope_does_not_infer_authority_or_ownership() -> None:
    scope = create_scope()

    assert not hasattr(
        scope,
        "authority",
    )

    assert not hasattr(
        scope,
        "owner",
    )

    assert not hasattr(
        scope,
        "institutional_subordination",
    )


def test_scope_does_not_require_customer_specific_taxonomy() -> None:
    scope = create_scope(
        commercial_channel_id="CUSTOMER-DEFINED-CHANNEL-X",
        point_of_sale_id="OPAQUE-LOCATION-47",
        department_id="CUSTOMER-DEFINED-DEPARTMENT-Z",
    )

    assert scope.commercial_channel_id == (
        "CUSTOMER-DEFINED-CHANNEL-X"
    )

    assert scope.point_of_sale_id == (
        "OPAQUE-LOCATION-47"
    )

    assert scope.department_id == (
        "CUSTOMER-DEFINED-DEPARTMENT-Z"
    )


def test_scope_does_not_infer_fixture_or_category_counts() -> None:
    scope = create_scope()

    assert not hasattr(
        scope,
        "fixture_count",
    )

    assert not hasattr(
        scope,
        "category_count",
    )

    assert not hasattr(
        scope,
        "presentation_capacity",
    )
