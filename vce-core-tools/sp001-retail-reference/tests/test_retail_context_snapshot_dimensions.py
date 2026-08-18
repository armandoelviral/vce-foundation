from dataclasses import FrozenInstanceError

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
    *,
    dimension_id: str,
    dimension_type: str,
    applicability: DimensionApplicability,
    evidence_status: DimensionEvidenceStatus,
    value: str | None = None,
) -> RetailContextDimension:
    return RetailContextDimension(
        dimension_id=dimension_id,
        dimension_type=dimension_type,
        applicability=applicability,
        evidence_status=evidence_status,
        value=value,
    )


def test_existing_snapshot_remains_valid_without_dimensions() -> None:
    snapshot = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
    )

    assert snapshot.dimensions == ()


def test_snapshot_preserves_one_customer_declared_dimension() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    snapshot = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
        dimensions=(department,),
    )

    assert snapshot.dimensions == (department,)
    assert snapshot.dimensions[0].value == "CHILDRENSWEAR"


def test_snapshot_preserves_multiple_independent_dimensions() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    fixture = build_dimension(
        dimension_id="CTX-FIXTURE-001",
        dimension_type="FIXTURE_TYPE",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.HUMAN_DECLARED,
        value="BACKWALL",
    )

    snapshot = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
        dimensions=(department, fixture),
    )

    assert len(snapshot.dimensions) == 2
    assert snapshot.dimensions[0] == department
    assert snapshot.dimensions[1] == fixture


def test_customers_may_define_different_dimension_sets() -> None:
    first_dimension = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    second_dimension = build_dimension(
        dimension_id="CTX-CUSTOM-001",
        dimension_type="CUSTOMER_DEFINED_COMMERCIAL_ZONE",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.HUMAN_DECLARED,
        value="ZONE-A",
    )

    first_snapshot = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
        dimensions=(first_dimension,),
    )

    second_snapshot = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-002",
        snapshot_version=1,
        case_id="CASE-002",
        dimensions=(second_dimension,),
    )

    assert (
        first_snapshot.dimensions[0].dimension_type
        == "DEPARTMENT"
    )

    assert (
        second_snapshot.dimensions[0].dimension_type
        == "CUSTOMER_DEFINED_COMMERCIAL_ZONE"
    )


def test_missing_required_dimension_value_remains_explicit() -> None:
    capacity = build_dimension(
        dimension_id="CTX-CAPACITY-001",
        dimension_type="PRESENTATION_CAPACITY",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    snapshot = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
        dimensions=(capacity,),
    )

    assert snapshot.dimensions[0].value is None

    assert (
        snapshot.dimensions[0].evidence_status
        is DimensionEvidenceStatus.NOT_PROVIDED
    )


def test_snapshot_dimension_collection_cannot_be_reassigned() -> None:
    snapshot = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
    )

    with pytest.raises(FrozenInstanceError):
        snapshot.dimensions = ()


def test_snapshot_dimension_collection_cannot_be_mutated() -> None:
    department = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    snapshot = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
        dimensions=(department,),
    )

    with pytest.raises(TypeError):
        snapshot.dimensions[0] = department


def test_new_snapshot_version_preserves_previous_context() -> None:
    original_dimension = build_dimension(
        dimension_id="CTX-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="CHILDRENSWEAR",
    )

    additional_dimension = build_dimension(
        dimension_id="CTX-FIXTURE-001",
        dimension_type="FIXTURE_TYPE",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="BACKWALL",
    )

    first = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=1,
        case_id="CASE-001",
        dimensions=(original_dimension,),
    )

    second = RetailContextSnapshot(
        snapshot_id="RCP-SNAPSHOT-001",
        snapshot_version=2,
        case_id="CASE-001",
        dimensions=(original_dimension, additional_dimension),
    )

    assert len(first.dimensions) == 1
    assert len(second.dimensions) == 2
    assert first.snapshot_version == 1
    assert second.snapshot_version == 2
