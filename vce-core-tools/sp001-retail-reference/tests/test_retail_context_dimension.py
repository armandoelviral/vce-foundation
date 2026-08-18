from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)


def test_dimension_preserves_explicit_identity_and_type() -> None:
    dimension = RetailContextDimension(
        dimension_id="CTX-AREA-001",
        dimension_type="FLOOR_AREA",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.MEASURED,
        value="120 m2",
    )

    assert dimension.dimension_id == "CTX-AREA-001"
    assert dimension.dimension_type == "FLOOR_AREA"
    assert dimension.value == "120 m2"


def test_customer_defined_dimension_type_is_supported() -> None:
    dimension = RetailContextDimension(
        dimension_id="CTX-CUSTOM-001",
        dimension_type="CUSTOMER_DEFINED_PRESENTATION_ZONE",
        applicability=DimensionApplicability.OPTIONAL,
        evidence_status=DimensionEvidenceStatus.HUMAN_DECLARED,
        value="ZONE-A",
    )

    assert dimension.dimension_type == (
        "CUSTOMER_DEFINED_PRESENTATION_ZONE"
    )
    assert dimension.applicability is DimensionApplicability.OPTIONAL


def test_required_dimension_can_preserve_missing_evidence() -> None:
    dimension = RetailContextDimension(
        dimension_id="CTX-CAPACITY-001",
        dimension_type="PRESENTATION_CAPACITY",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    assert dimension.applicability is DimensionApplicability.REQUIRED
    assert (
        dimension.evidence_status
        is DimensionEvidenceStatus.NOT_PROVIDED
    )
    assert dimension.value is None


def test_not_applicable_dimension_is_explicit() -> None:
    dimension = RetailContextDimension(
        dimension_id="CTX-CLUSTER-001",
        dimension_type="COMMERCIAL_CLUSTER",
        applicability=DimensionApplicability.NOT_APPLICABLE,
        evidence_status=DimensionEvidenceStatus.NOT_PROVIDED,
    )

    assert (
        dimension.applicability
        is DimensionApplicability.NOT_APPLICABLE
    )
    assert dimension.value is None


def test_disputed_dimension_preserves_conflicting_context() -> None:
    dimension = RetailContextDimension(
        dimension_id="CTX-DEPARTMENT-001",
        dimension_type="DEPARTMENT",
        applicability=DimensionApplicability.DISPUTED,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value="DECLARED_CONTEXT_UNVERIFIED",
    )

    assert dimension.applicability is DimensionApplicability.DISPUTED
    assert dimension.evidence_status is DimensionEvidenceStatus.DISPUTED


def test_dimension_preserves_human_declared_provenance() -> None:
    dimension = RetailContextDimension(
        dimension_id="CTX-FIXTURE-001",
        dimension_type="FIXTURE_TYPE",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.HUMAN_DECLARED,
        value="BACKWALL",
    )

    assert (
        dimension.evidence_status
        is DimensionEvidenceStatus.HUMAN_DECLARED
    )
    assert (
        dimension.evidence_status
        is not DimensionEvidenceStatus.INDEPENDENTLY_VERIFIED
    )


def test_dimension_is_immutable() -> None:
    dimension = RetailContextDimension(
        dimension_id="CTX-CATEGORY-001",
        dimension_type="ACTIVE_CATEGORY",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="TODDLER_BOYS",
    )

    with pytest.raises(FrozenInstanceError):
        dimension.value = "BIG_BOYS"


def test_applicability_vocabulary_is_exact() -> None:
    assert {
        state.value
        for state in DimensionApplicability
    } == {
        "REQUIRED",
        "OPTIONAL",
        "NOT_APPLICABLE",
        "DISPUTED",
    }


def test_evidence_status_vocabulary_is_exact() -> None:
    assert {
        state.value
        for state in DimensionEvidenceStatus
    } == {
        "DOCUMENTED",
        "HUMAN_DECLARED",
        "MEASURED",
        "INDEPENDENTLY_VERIFIED",
        "NOT_PROVIDED",
        "INSUFFICIENT_EVIDENCE",
        "DISPUTED",
    }
