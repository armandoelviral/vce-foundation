import pytest

from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)


def build_dimension(
    dimension_id: str,
    dimension_type: str = "FIXTURE_TYPE",
) -> RetailContextDimension:
    return RetailContextDimension(
        dimension_id=dimension_id,
        dimension_type=dimension_type,
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="BACKWALL",
    )


def test_snapshot_rejects_empty_snapshot_identity() -> None:
    with pytest.raises(
        ValueError,
        match="snapshot_id must not be empty",
    ):
        RetailContextSnapshot(
            snapshot_id="",
            snapshot_version=1,
            case_id="CASE-001",
        )


def test_snapshot_rejects_blank_snapshot_identity() -> None:
    with pytest.raises(
        ValueError,
        match="snapshot_id must not be empty",
    ):
        RetailContextSnapshot(
            snapshot_id="   ",
            snapshot_version=1,
            case_id="CASE-001",
        )


def test_snapshot_rejects_empty_case_identity() -> None:
    with pytest.raises(
        ValueError,
        match="case_id must not be empty",
    ):
        RetailContextSnapshot(
            snapshot_id="RCP-SNAPSHOT-001",
            snapshot_version=1,
            case_id="",
        )


def test_snapshot_rejects_blank_case_identity() -> None:
    with pytest.raises(
        ValueError,
        match="case_id must not be empty",
    ):
        RetailContextSnapshot(
            snapshot_id="RCP-SNAPSHOT-001",
            snapshot_version=1,
            case_id="   ",
        )


def test_snapshot_rejects_zero_version() -> None:
    with pytest.raises(
        ValueError,
        match="snapshot_version must be a positive integer",
    ):
        RetailContextSnapshot(
            snapshot_id="RCP-SNAPSHOT-001",
            snapshot_version=0,
            case_id="CASE-001",
        )


def test_snapshot_rejects_negative_version() -> None:
    with pytest.raises(
        ValueError,
        match="snapshot_version must be a positive integer",
    ):
        RetailContextSnapshot(
            snapshot_id="RCP-SNAPSHOT-001",
            snapshot_version=-1,
            case_id="CASE-001",
        )


def test_snapshot_rejects_boolean_version() -> None:
    with pytest.raises(
        ValueError,
        match="snapshot_version must be a positive integer",
    ):
        RetailContextSnapshot(
            snapshot_id="RCP-SNAPSHOT-001",
            snapshot_version=True,
            case_id="CASE-001",
        )


def test_snapshot_rejects_mutable_dimension_collection() -> None:
    dimension = build_dimension(
        dimension_id="CTX-FIXTURE-001",
    )

    with pytest.raises(
        TypeError,
        match="dimensions must be an immutable tuple",
    ):
        RetailContextSnapshot(
            snapshot_id="RCP-SNAPSHOT-001",
            snapshot_version=1,
            case_id="CASE-001",
            dimensions=[dimension],
        )


def test_snapshot_rejects_non_dimension_elements() -> None:
    with pytest.raises(
        TypeError,
        match="every dimension must be a RetailContextDimension",
    ):
        RetailContextSnapshot(
            snapshot_id="RCP-SNAPSHOT-001",
            snapshot_version=1,
            case_id="CASE-001",
            dimensions=("CTX-FIXTURE-001",),
        )


def test_snapshot_rejects_duplicate_dimension_identity() -> None:
    first = build_dimension(
        dimension_id="CTX-FIXTURE-001",
    )

    duplicate = build_dimension(
        dimension_id="CTX-FIXTURE-001",
        dimension_type="PRESENTATION_CAPACITY",
    )

    with pytest.raises(
        ValueError,
        match="duplicate dimension_id: CTX-FIXTURE-001",
    ):
        RetailContextSnapshot(
            snapshot_id="RCP-SNAPSHOT-001",
            snapshot_version=1,
            case_id="CASE-001",
            dimensions=(first, duplicate),
        )


def test_snapshot_allows_multiple_dimensions_of_same_type() -> None:
    first_fixture = build_dimension(
        dimension_id="CTX-FIXTURE-001",
    )

    second_fixture = build_dimension(
        dimension_id="CTX-FIXTURE-002",
    )

    snapshot = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
        dimensions=(first_fixture, second_fixture),
    )

    assert len(snapshot.dimensions) == 2

    assert {
        dimension.dimension_id
        for dimension in snapshot.dimensions
    } == {
        "CTX-FIXTURE-001",
        "CTX-FIXTURE-002",
    }

    assert {
        dimension.dimension_type
        for dimension in snapshot.dimensions
    } == {
        "FIXTURE_TYPE",
    }


def test_snapshot_preserves_valid_dimension_order() -> None:
    first = build_dimension(
        dimension_id="CTX-FIXTURE-002",
    )

    second = build_dimension(
        dimension_id="CTX-FIXTURE-001",
    )

    snapshot = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
        dimensions=(first, second),
    )

    assert tuple(
        dimension.dimension_id
        for dimension in snapshot.dimensions
    ) == (
        "CTX-FIXTURE-002",
        "CTX-FIXTURE-001",
    )
