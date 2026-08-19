import pytest

from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)


def build_dimension(
    *,
    dimension_id: str = "CTX-FIXTURE-001",
    dimension_type: str = "FIXTURE_TYPE",
    applicability: DimensionApplicability = (
        DimensionApplicability.REQUIRED
    ),
    evidence_status: DimensionEvidenceStatus = (
        DimensionEvidenceStatus.DOCUMENTED
    ),
    value: str | None = "BACKWALL",
) -> RetailContextDimension:
    return RetailContextDimension(
        dimension_id=dimension_id,
        dimension_type=dimension_type,
        applicability=applicability,
        evidence_status=evidence_status,
        value=value,
    )


@pytest.mark.parametrize(
    "invalid_identity",
    ("", "   "),
)
def test_dimension_rejects_invalid_identity(
    invalid_identity: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="dimension_id must not be empty",
    ):
        build_dimension(
            dimension_id=invalid_identity,
        )


@pytest.mark.parametrize(
    "invalid_type",
    ("", "   "),
)
def test_dimension_rejects_invalid_type(
    invalid_type: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="dimension_type must not be empty",
    ):
        build_dimension(
            dimension_type=invalid_type,
        )


def test_dimension_rejects_untyped_applicability() -> None:
    with pytest.raises(
        TypeError,
        match="applicability must be a DimensionApplicability",
    ):
        build_dimension(
            applicability="REQUIRED",
        )


def test_dimension_rejects_untyped_evidence_status() -> None:
    with pytest.raises(
        TypeError,
        match="evidence_status must be a DimensionEvidenceStatus",
    ):
        build_dimension(
            evidence_status="DOCUMENTED",
        )


def test_not_provided_evidence_rejects_value() -> None:
    with pytest.raises(
        ValueError,
        match="NOT_PROVIDED evidence cannot contain a value",
    ):
        build_dimension(
            evidence_status=(
                DimensionEvidenceStatus.NOT_PROVIDED
            ),
            value="BACKWALL",
        )


@pytest.mark.parametrize(
    "evidence_status",
    (
        DimensionEvidenceStatus.DOCUMENTED,
        DimensionEvidenceStatus.HUMAN_DECLARED,
        DimensionEvidenceStatus.MEASURED,
        DimensionEvidenceStatus.INDEPENDENTLY_VERIFIED,
    ),
)
def test_supported_evidence_requires_value(
    evidence_status: DimensionEvidenceStatus,
) -> None:
    with pytest.raises(
        ValueError,
        match="documented evidence requires a value",
    ):
        build_dimension(
            evidence_status=evidence_status,
            value=None,
        )


def test_insufficient_evidence_allows_missing_value() -> None:
    dimension = build_dimension(
        evidence_status=(
            DimensionEvidenceStatus.INSUFFICIENT_EVIDENCE
        ),
        value=None,
    )

    assert dimension.value is None


def test_insufficient_evidence_preserves_partial_value() -> None:
    dimension = build_dimension(
        evidence_status=(
            DimensionEvidenceStatus.INSUFFICIENT_EVIDENCE
        ),
        value="UNVERIFIED_CAPACITY",
    )

    assert dimension.value == "UNVERIFIED_CAPACITY"


def test_disputed_evidence_preserves_contested_value() -> None:
    dimension = build_dimension(
        applicability=DimensionApplicability.DISPUTED,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value="DECLARED_CONTEXT_UNVERIFIED",
    )

    assert dimension.value == "DECLARED_CONTEXT_UNVERIFIED"


def test_disputed_evidence_allows_missing_value() -> None:
    dimension = build_dimension(
        applicability=DimensionApplicability.DISPUTED,
        evidence_status=DimensionEvidenceStatus.DISPUTED,
        value=None,
    )

    assert dimension.value is None


def test_not_applicable_dimension_rejects_operational_value() -> None:
    with pytest.raises(
        ValueError,
        match="NOT_APPLICABLE dimensions cannot contain a value",
    ):
        build_dimension(
            applicability=(
                DimensionApplicability.NOT_APPLICABLE
            ),
            evidence_status=(
                DimensionEvidenceStatus.DOCUMENTED
            ),
            value="BACKWALL",
        )


def test_not_applicable_dimension_preserves_missing_evidence() -> None:
    dimension = build_dimension(
        applicability=(
            DimensionApplicability.NOT_APPLICABLE
        ),
        evidence_status=(
            DimensionEvidenceStatus.NOT_PROVIDED
        ),
        value=None,
    )

    assert (
        dimension.applicability
        is DimensionApplicability.NOT_APPLICABLE
    )

    assert dimension.value is None


def test_customer_defined_dimension_type_remains_allowed() -> None:
    dimension = build_dimension(
        dimension_type=(
            "CUSTOMER_DEFINED_COMMERCIAL_SEGMENT"
        ),
    )

    assert (
        dimension.dimension_type
        == "CUSTOMER_DEFINED_COMMERCIAL_SEGMENT"
    )
