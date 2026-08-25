from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.contracts.retail_context_definition import (
    RetailContextDefinition,
)
from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
)
from sp001.contracts.retail_context_snapshot_completeness import (
    SnapshotCompletenessStatus,
)
from sp001.services.retail_context_assessment import (
    RetailContextAssessmentResult,
)
from sp001.services.retail_context_assessment_completeness_report import (
    RetailContextAssessmentCompletenessReport,
    build_retail_context_assessment_completeness_report,
)
from sp001.services.retail_context_assessment_report import (
    RetailContextAssessmentReport,
    build_retail_context_assessment_report,
)
from sp001.services.retail_context_assessment_report_payload_validation import (
    validate_retail_context_assessment_report_payload,
)
from sp001.services.retail_context_assessment_report_serialization import (
    serialize_retail_context_assessment_report,
)

from test_retail_context_assessment_completeness import (
    complete_required_dimensions,
    create_assessment,
    create_definition,
    create_dimension,
    create_snapshot,
)


def create_report(
    *,
    result: RetailContextAssessmentResult,
) -> RetailContextAssessmentCompletenessReport:
    return build_retail_context_assessment_completeness_report(
        result=result,
    )


def test_completeness_report_returns_independent_immutable_contract() -> None:
    report = create_report(
        result=create_assessment(
            snapshot=create_snapshot(),
        ),
    )

    assert isinstance(
        report,
        RetailContextAssessmentCompletenessReport,
    )


def test_completeness_report_has_exact_sanitized_field_contract() -> None:
    assert tuple(
        field.name
        for field in fields(
            RetailContextAssessmentCompletenessReport,
        )
    ) == (
        "case_id",
        "snapshot_id",
        "snapshot_version",
        "context_definition_id",
        "definition_version",
        "context_completeness_status",
        "required_dimension_types",
        "missing_required_dimension_types",
        "insufficient_evidence_dimension_types",
        "disputed_dimension_types",
    )


def test_completeness_report_rejects_invalid_assessment_result() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "result must be a "
            "RetailContextAssessmentResult"
        ),
    ):
        build_retail_context_assessment_completeness_report(
            result=None,
        )


def test_completeness_report_preserves_case_identity() -> None:
    result = create_assessment(
        snapshot=create_snapshot(),
    )

    report = create_report(
        result=result,
    )

    assert report.case_id == (
        result.snapshot.case_id
    )


def test_completeness_report_preserves_snapshot_identity_and_version() -> None:
    result = create_assessment(
        snapshot=create_snapshot(),
    )

    report = create_report(
        result=result,
    )

    assert report.snapshot_id == (
        result.snapshot.snapshot_id
    )
    assert report.snapshot_version == (
        result.snapshot.snapshot_version
    )


def test_completeness_report_preserves_definition_identity_and_version() -> None:
    definition = create_definition(
        context_definition_id="RCP-DEFINITION-VERSIONED",
        definition_version=9,
    )

    report = create_report(
        result=create_assessment(
            snapshot=create_snapshot(
                context_definition=definition,
            ),
        ),
    )

    assert report.context_definition_id == (
        "RCP-DEFINITION-VERSIONED"
    )
    assert report.definition_version == 9


def test_snapshot_without_definition_remains_not_established() -> None:
    report = create_report(
        result=create_assessment(
            snapshot=create_snapshot(),
        ),
    )

    assert report.context_completeness_status is (
        SnapshotCompletenessStatus.NOT_ESTABLISHED
    )
    assert report.context_definition_id is None
    assert report.definition_version is None


def test_historical_unclassified_definition_remains_not_established() -> None:
    definition = RetailContextDefinition(
        context_definition_id="RCP-DEFINITION-HISTORICAL",
        customer_id="CUSTOMER-001",
        definition_version=1,
        dimension_types=(
            "DEPARTMENT",
            "INVENTORY_STATE",
        ),
    )

    report = create_report(
        result=create_assessment(
            snapshot=create_snapshot(
                context_definition=definition,
            ),
        ),
    )

    assert report.context_completeness_status is (
        SnapshotCompletenessStatus.NOT_ESTABLISHED
    )
    assert report.context_definition_id == (
        "RCP-DEFINITION-HISTORICAL"
    )
    assert report.definition_version == 1


def test_historical_result_without_completeness_remains_not_established() -> None:
    current = create_assessment(
        snapshot=create_snapshot(
            context_definition=create_definition(),
        ),
    )

    historical = RetailContextAssessmentResult(
        snapshot=current.snapshot,
        provenance_graph=current.provenance_graph,
        summary=current.summary,
    )

    report = create_report(
        result=historical,
    )

    assert report.context_completeness_status is (
        SnapshotCompletenessStatus.NOT_ESTABLISHED
    )
    assert report.required_dimension_types == ()
    assert report.missing_required_dimension_types == ()
    assert report.insufficient_evidence_dimension_types == ()
    assert report.disputed_dimension_types == ()


def test_complete_required_context_is_reported() -> None:
    report = create_report(
        result=create_assessment(
            snapshot=create_snapshot(
                context_definition=create_definition(),
                dimensions=complete_required_dimensions(),
            ),
        ),
    )

    assert report.context_completeness_status is (
        SnapshotCompletenessStatus.COMPLETE
    )
    assert report.required_dimension_types == (
        "DEPARTMENT",
        "INVENTORY_STATE",
    )


def test_incomplete_required_context_preserves_missing_types() -> None:
    report = create_report(
        result=create_assessment(
            snapshot=create_snapshot(
                context_definition=create_definition(),
                dimensions=(),
            ),
        ),
    )

    assert report.context_completeness_status is (
        SnapshotCompletenessStatus.INCOMPLETE
    )
    assert report.missing_required_dimension_types == (
        "DEPARTMENT",
        "INVENTORY_STATE",
    )


def test_insufficient_required_evidence_is_reported_separately() -> None:
    report = create_report(
        result=create_assessment(
            snapshot=create_snapshot(
                context_definition=create_definition(),
                dimensions=(
                    create_dimension(
                        dimension_id="DIM-DEPARTMENT",
                        dimension_type="DEPARTMENT",
                    ),
                    create_dimension(
                        dimension_id="DIM-INVENTORY",
                        dimension_type="INVENTORY_STATE",
                        evidence_status=(
                            DimensionEvidenceStatus.NOT_PROVIDED
                        ),
                        value=None,
                    ),
                ),
            ),
        ),
    )

    assert report.context_completeness_status is (
        SnapshotCompletenessStatus.INDETERMINATE
    )
    assert report.missing_required_dimension_types == ()
    assert report.insufficient_evidence_dimension_types == (
        "INVENTORY_STATE",
    )


def test_disputed_required_evidence_is_reported_separately() -> None:
    report = create_report(
        result=create_assessment(
            snapshot=create_snapshot(
                context_definition=create_definition(),
                dimensions=(
                    create_dimension(
                        dimension_id="DIM-DEPARTMENT",
                        dimension_type="DEPARTMENT",
                    ),
                    create_dimension(
                        dimension_id="DIM-INVENTORY",
                        dimension_type="INVENTORY_STATE",
                        evidence_status=(
                            DimensionEvidenceStatus.DISPUTED
                        ),
                        value=None,
                    ),
                ),
            ),
        ),
    )

    assert report.context_completeness_status is (
        SnapshotCompletenessStatus.INDETERMINATE
    )
    assert report.disputed_dimension_types == (
        "INVENTORY_STATE",
    )


def test_disputed_required_context_preserves_missing_context() -> None:
    report = create_report(
        result=create_assessment(
            snapshot=create_snapshot(
                context_definition=create_definition(),
                dimensions=(
                    create_dimension(
                        dimension_id="DIM-DEPARTMENT",
                        dimension_type="DEPARTMENT",
                        evidence_status=(
                            DimensionEvidenceStatus.DISPUTED
                        ),
                        value=None,
                    ),
                ),
            ),
        ),
    )

    assert report.context_completeness_status is (
        SnapshotCompletenessStatus.INDETERMINATE
    )
    assert report.disputed_dimension_types == (
        "DEPARTMENT",
    )
    assert report.missing_required_dimension_types == (
        "INVENTORY_STATE",
    )


def test_optional_dimension_absence_does_not_block_completeness() -> None:
    report = create_report(
        result=create_assessment(
            snapshot=create_snapshot(
                context_definition=create_definition(),
                dimensions=complete_required_dimensions(),
            ),
        ),
    )

    assert report.context_completeness_status is (
        SnapshotCompletenessStatus.COMPLETE
    )
    assert "PRESENTATION_CAPACITY" not in (
        report.missing_required_dimension_types
    )


def test_optional_disputed_dimension_does_not_block_completeness() -> None:
    report = create_report(
        result=create_assessment(
            snapshot=create_snapshot(
                context_definition=create_definition(),
                dimensions=(
                    *complete_required_dimensions(),
                    create_dimension(
                        dimension_id="DIM-CAPACITY",
                        dimension_type="PRESENTATION_CAPACITY",
                        applicability=(
                            DimensionApplicability.DISPUTED
                        ),
                        evidence_status=(
                            DimensionEvidenceStatus.DISPUTED
                        ),
                        value=None,
                    ),
                ),
            ),
        ),
    )

    assert report.context_completeness_status is (
        SnapshotCompletenessStatus.COMPLETE
    )
    assert report.disputed_dimension_types == ()


def test_customer_requirement_order_is_preserved() -> None:
    report = create_report(
        result=create_assessment(
            snapshot=create_snapshot(
                context_definition=create_definition(),
                dimensions=(),
            ),
        ),
    )

    assert report.required_dimension_types == (
        "DEPARTMENT",
        "INVENTORY_STATE",
    )
    assert report.missing_required_dimension_types == (
        "DEPARTMENT",
        "INVENTORY_STATE",
    )


def test_completeness_report_is_immutable() -> None:
    report = create_report(
        result=create_assessment(
            snapshot=create_snapshot(),
        ),
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        report.context_completeness_status = (
            SnapshotCompletenessStatus.COMPLETE
        )


def test_canonical_assessment_report_preserves_exact_twenty_fields() -> None:
    result = create_assessment(
        snapshot=create_snapshot(
            context_definition=create_definition(),
            dimensions=(),
        ),
    )

    create_report(
        result=result,
    )

    canonical_report = build_retail_context_assessment_report(
        result=result,
    )

    assert isinstance(
        canonical_report,
        RetailContextAssessmentReport,
    )
    assert len(
        fields(
            RetailContextAssessmentReport,
        )
    ) == 20


def test_canonical_report_payload_remains_valid_and_unchanged() -> None:
    result = create_assessment(
        snapshot=create_snapshot(
            context_definition=create_definition(),
            dimensions=(),
        ),
    )

    create_report(
        result=result,
    )

    canonical_report = build_retail_context_assessment_report(
        result=result,
    )

    payload = serialize_retail_context_assessment_report(
        report=canonical_report,
    )

    assert validate_retail_context_assessment_report_payload(
        payload=payload,
    ) is True


def test_completeness_report_does_not_infer_commercial_claims() -> None:
    report = create_report(
        result=create_assessment(
            snapshot=create_snapshot(
                context_definition=create_definition(),
            ),
        ),
    )

    for attribute in (
        "customer_acceptance_status",
        "commercial_impact_status",
        "independent_intervention_status",
        "compliance_status",
        "authority",
        "owner",
        "inferred_values",
    ):
        assert not hasattr(
            report,
            attribute,
        )


def test_completeness_report_does_not_mutate_source_snapshot() -> None:
    snapshot = create_snapshot(
        context_definition=create_definition(),
        dimensions=(),
    )

    original_dimensions = snapshot.dimensions

    report = create_report(
        result=create_assessment(
            snapshot=snapshot,
        ),
    )

    assert snapshot.dimensions is original_dimensions
    assert snapshot.dimensions == ()
    assert report.missing_required_dimension_types == (
        "DEPARTMENT",
        "INVENTORY_STATE",
    )
