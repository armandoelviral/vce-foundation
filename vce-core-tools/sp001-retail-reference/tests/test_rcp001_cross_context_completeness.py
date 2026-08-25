from dataclasses import dataclass, replace

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
from sp001.contracts.retail_context_snapshot_completeness import (
    SnapshotCompletenessStatus,
)
from sp001.services.retail_context_assessment import (
    RetailContextAssessmentResult,
    execute_retail_context_assessment,
)
from sp001.services.retail_context_assessment_completeness_report import (
    RetailContextAssessmentCompletenessReport,
    build_retail_context_assessment_completeness_report,
)
from sp001.services.retail_context_assessment_report import (
    build_retail_context_assessment_report,
)
from sp001.services.retail_context_assessment_report_payload_validation import (
    validate_retail_context_assessment_report_payload,
)
from sp001.services.retail_context_assessment_report_serialization import (
    serialize_retail_context_assessment_report,
)

from test_rcp001_tcp_sears_canonical_matrix import (
    create_canonical_comparisons,
    create_canonical_graph,
)


@dataclass(frozen=True, slots=True)
class CrossContextPair:
    """Two independent store assessments sharing canonical evidence."""

    shared_dimension: RetailContextDimension
    result_a: RetailContextAssessmentResult
    result_b: RetailContextAssessmentResult
    report_a: RetailContextAssessmentCompletenessReport
    report_b: RetailContextAssessmentCompletenessReport


@pytest.fixture(
    scope="module",
)
def context_pair() -> CrossContextPair:
    shared_dimension = RetailContextDimension(
        dimension_id="DIM-DEPARTMENT-SHARED",
        dimension_type="DEPARTMENT",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="GIRLS",
    )

    scope_a = RetailContextScope(
        context_id="CONTEXT-STORE-A",
        commercial_channel_id="DEPARTMENT_STORE",
        point_of_sale_id="STORE-A",
        department_id="GIRLS",
        profile_version=1,
    )

    scope_b = RetailContextScope(
        context_id="CONTEXT-STORE-B",
        commercial_channel_id="DEPARTMENT_STORE",
        point_of_sale_id="STORE-B",
        department_id="GIRLS",
        profile_version=1,
    )

    definition_a = RetailContextDefinition(
        context_definition_id="DEFINITION-CUSTOMER-A",
        customer_id="CUSTOMER-A",
        definition_version=1,
        dimension_types=(
            "DEPARTMENT",
            "INVENTORY_STATE",
        ),
        required_dimension_types=(
            "DEPARTMENT",
        ),
        optional_dimension_types=(
            "INVENTORY_STATE",
        ),
    )

    definition_b = RetailContextDefinition(
        context_definition_id="DEFINITION-CUSTOMER-B",
        customer_id="CUSTOMER-B",
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

    snapshot_a = RetailContextSnapshot(
        snapshot_id="SNAPSHOT-STORE-A",
        snapshot_version=1,
        case_id="CASE-STORE-A",
        context_scope=scope_a,
        context_definition=definition_a,
        dimensions=(
            shared_dimension,
        ),
    )

    snapshot_b = RetailContextSnapshot(
        snapshot_id="SNAPSHOT-STORE-B",
        snapshot_version=1,
        case_id="CASE-STORE-B",
        context_scope=scope_b,
        context_definition=definition_b,
        dimensions=(
            shared_dimension,
        ),
    )

    canonical_comparisons = (
        create_canonical_comparisons()
    )

    comparisons_a = tuple(
        replace(
            comparison,
            case_id=snapshot_a.case_id,
            snapshot_id=snapshot_a.snapshot_id,
            snapshot_version=snapshot_a.snapshot_version,
        )
        for comparison in canonical_comparisons
    )

    comparisons_b = tuple(
        replace(
            comparison,
            case_id=snapshot_b.case_id,
            snapshot_id=snapshot_b.snapshot_id,
            snapshot_version=snapshot_b.snapshot_version,
        )
        for comparison in canonical_comparisons
    )

    canonical_graph = create_canonical_graph()

    result_a = execute_retail_context_assessment(
        snapshot=snapshot_a,
        comparisons=comparisons_a,
        provenance_records=canonical_graph.records,
        context_policy_ids=canonical_graph.context_policy_ids,
    )

    result_b = execute_retail_context_assessment(
        snapshot=snapshot_b,
        comparisons=comparisons_b,
        provenance_records=canonical_graph.records,
        context_policy_ids=canonical_graph.context_policy_ids,
    )

    report_a = (
        build_retail_context_assessment_completeness_report(
            result=result_a,
        )
    )

    report_b = (
        build_retail_context_assessment_completeness_report(
            result=result_b,
        )
    )

    return CrossContextPair(
        shared_dimension=shared_dimension,
        result_a=result_a,
        result_b=result_b,
        report_a=report_a,
        report_b=report_b,
    )


def test_store_snapshots_share_exact_dimension_object(
    context_pair: CrossContextPair,
) -> None:
    assert context_pair.result_a.snapshot.dimensions[0] is (
        context_pair.shared_dimension
    )
    assert context_pair.result_b.snapshot.dimensions[0] is (
        context_pair.shared_dimension
    )


def test_shared_dimension_preserves_identity_and_value(
    context_pair: CrossContextPair,
) -> None:
    assert context_pair.shared_dimension.dimension_id == (
        "DIM-DEPARTMENT-SHARED"
    )
    assert context_pair.shared_dimension.dimension_type == (
        "DEPARTMENT"
    )
    assert context_pair.shared_dimension.value == "GIRLS"


def test_rule_evidence_references_are_identical_across_stores(
    context_pair: CrossContextPair,
) -> None:
    evidence_a = tuple(
        (
            comparison.initial_evidence_ids,
            comparison.final_evidence_ids,
        )
        for comparison in (
            context_pair.result_a.summary.comparisons
        )
    )

    evidence_b = tuple(
        (
            comparison.initial_evidence_ids,
            comparison.final_evidence_ids,
        )
        for comparison in (
            context_pair.result_b.summary.comparisons
        )
    )

    assert evidence_a == evidence_b


def test_rule_identities_are_identical_across_stores(
    context_pair: CrossContextPair,
) -> None:
    rule_ids_a = tuple(
        comparison.rule_id
        for comparison in (
            context_pair.result_a.summary.comparisons
        )
    )

    rule_ids_b = tuple(
        comparison.rule_id
        for comparison in (
            context_pair.result_b.summary.comparisons
        )
    )

    assert rule_ids_a == rule_ids_b
    assert len(
        rule_ids_a,
    ) == 35


def test_case_identities_remain_distinct(
    context_pair: CrossContextPair,
) -> None:
    assert context_pair.result_a.snapshot.case_id == (
        "CASE-STORE-A"
    )
    assert context_pair.result_b.snapshot.case_id == (
        "CASE-STORE-B"
    )


def test_snapshot_identities_remain_distinct(
    context_pair: CrossContextPair,
) -> None:
    assert context_pair.result_a.snapshot.snapshot_id == (
        "SNAPSHOT-STORE-A"
    )
    assert context_pair.result_b.snapshot.snapshot_id == (
        "SNAPSHOT-STORE-B"
    )


def test_stores_share_declared_commercial_channel(
    context_pair: CrossContextPair,
) -> None:
    scope_a = context_pair.result_a.snapshot.context_scope
    scope_b = context_pair.result_b.snapshot.context_scope

    assert scope_a.commercial_channel_id == (
        "DEPARTMENT_STORE"
    )
    assert scope_a.commercial_channel_id == (
        scope_b.commercial_channel_id
    )


def test_stores_share_declared_department(
    context_pair: CrossContextPair,
) -> None:
    scope_a = context_pair.result_a.snapshot.context_scope
    scope_b = context_pair.result_b.snapshot.context_scope

    assert scope_a.department_id == "GIRLS"
    assert scope_a.department_id == (
        scope_b.department_id
    )


def test_point_of_sale_identities_remain_distinct(
    context_pair: CrossContextPair,
) -> None:
    scope_a = context_pair.result_a.snapshot.context_scope
    scope_b = context_pair.result_b.snapshot.context_scope

    assert scope_a.point_of_sale_id == "STORE-A"
    assert scope_b.point_of_sale_id == "STORE-B"
    assert scope_a.context_id != scope_b.context_id


def test_customer_identities_remain_distinct(
    context_pair: CrossContextPair,
) -> None:
    definition_a = (
        context_pair.result_a.snapshot.context_definition
    )
    definition_b = (
        context_pair.result_b.snapshot.context_definition
    )

    assert definition_a.customer_id == "CUSTOMER-A"
    assert definition_b.customer_id == "CUSTOMER-B"


def test_customers_define_distinct_required_context(
    context_pair: CrossContextPair,
) -> None:
    definition_a = (
        context_pair.result_a.snapshot.context_definition
    )
    definition_b = (
        context_pair.result_b.snapshot.context_definition
    )

    assert definition_a.required_dimension_types == (
        "DEPARTMENT",
    )
    assert definition_b.required_dimension_types == (
        "DEPARTMENT",
        "INVENTORY_STATE",
    )


def test_store_a_is_complete_with_shared_department_evidence(
    context_pair: CrossContextPair,
) -> None:
    assert context_pair.result_a.context_completeness.status is (
        SnapshotCompletenessStatus.COMPLETE
    )


def test_store_b_is_incomplete_with_identical_department_evidence(
    context_pair: CrossContextPair,
) -> None:
    assert context_pair.result_b.context_completeness.status is (
        SnapshotCompletenessStatus.INCOMPLETE
    )


def test_store_b_reports_only_missing_inventory_context(
    context_pair: CrossContextPair,
) -> None:
    assert (
        context_pair.result_b.context_completeness
        .missing_required_dimension_types
    ) == (
        "INVENTORY_STATE",
    )

    assert (
        context_pair.result_a.context_completeness
        .missing_required_dimension_types
    ) == ()


def test_missing_inventory_is_not_synthesized(
    context_pair: CrossContextPair,
) -> None:
    dimensions_a = (
        context_pair.result_a.snapshot.dimensions
    )
    dimensions_b = (
        context_pair.result_b.snapshot.dimensions
    )

    assert len(
        dimensions_a,
    ) == 1
    assert len(
        dimensions_b,
    ) == 1
    assert all(
        dimension.dimension_type != "INVENTORY_STATE"
        for dimension in dimensions_b
    )


def test_rule_accounting_remains_identical_across_contexts(
    context_pair: CrossContextPair,
) -> None:
    assert context_pair.result_a.provenance_graph.total_rules == 35
    assert context_pair.result_b.provenance_graph.total_rules == 35

    assert context_pair.result_a.summary.total_improved_count == 14
    assert context_pair.result_b.summary.total_improved_count == 14


def test_complementary_reports_preserve_context_divergence(
    context_pair: CrossContextPair,
) -> None:
    assert context_pair.report_a.context_completeness_status is (
        SnapshotCompletenessStatus.COMPLETE
    )
    assert context_pair.report_b.context_completeness_status is (
        SnapshotCompletenessStatus.INCOMPLETE
    )


def test_complementary_reports_preserve_definition_identity(
    context_pair: CrossContextPair,
) -> None:
    assert context_pair.report_a.context_definition_id == (
        "DEFINITION-CUSTOMER-A"
    )
    assert context_pair.report_b.context_definition_id == (
        "DEFINITION-CUSTOMER-B"
    )


def test_complementary_reports_do_not_yet_export_store_scope(
    context_pair: CrossContextPair,
) -> None:
    for report in (
        context_pair.report_a,
        context_pair.report_b,
    ):
        assert not hasattr(
            report,
            "point_of_sale_id",
        )
        assert not hasattr(
            report,
            "context_id",
        )
        assert not hasattr(
            report,
            "customer_id",
        )


def test_canonical_exchange_reports_remain_valid_for_both_stores(
    context_pair: CrossContextPair,
) -> None:
    for result in (
        context_pair.result_a,
        context_pair.result_b,
    ):
        report = build_retail_context_assessment_report(
            result=result,
        )

        payload = serialize_retail_context_assessment_report(
            report=report,
        )

        assert validate_retail_context_assessment_report_payload(
            payload=payload,
        ) is True

        assert report.customer_acceptance_status == (
            "NOT_ESTABLISHED"
        )
        assert report.commercial_impact_status == (
            "NOT_ESTABLISHED"
        )
