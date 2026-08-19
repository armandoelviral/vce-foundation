import importlib.util
from pathlib import Path

from sp001.contracts.retail_context_dependency_source import (
    DependencySourceType,
)
from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
)
from sp001.contracts.retail_context_rule_observation_comparison import (
    ObservationChangeStatus,
)
from sp001.contracts.retail_context_rule_provenance import (
    RuleProvenanceType,
)
from sp001.services.retail_context_assessment import (
    RetailContextAssessmentResult,
    execute_retail_context_assessment,
)


def load_canonical_matrix():
    path = (
        Path(__file__).resolve().parent
        / "test_rcp001_tcp_sears_canonical_matrix.py"
    )

    specification = importlib.util.spec_from_file_location(
        "rcp001_tcp_sears_canonical_matrix",
        path,
    )

    if (
        specification is None
        or specification.loader is None
    ):
        raise RuntimeError(
            "canonical TCP/Sears matrix module unavailable"
        )

    module = importlib.util.module_from_spec(
        specification,
    )

    specification.loader.exec_module(
        module,
    )

    return module


CANONICAL = load_canonical_matrix()


def execute_canonical_assessment():
    case = CANONICAL.create_case()

    context_snapshot = CANONICAL.create_snapshot(
        case.case_id,
    )

    comparisons = CANONICAL.create_canonical_comparisons()

    provenance_records = tuple(
        CANONICAL.create_provenance(
            rule_id,
        )
        for rule_id in CANONICAL.CANONICAL_RULE_IDS
    )

    return execute_retail_context_assessment(
        snapshot=context_snapshot,
        comparisons=comparisons,
        provenance_records=provenance_records,
        context_policy_ids=(
            CANONICAL.CONTEXT_POLICY_ID,
        ),
    )


def test_service_executes_complete_tcp_sears_assessment() -> None:
    result = execute_canonical_assessment()

    assert isinstance(
        result,
        RetailContextAssessmentResult,
    )


def test_service_preserves_canonical_case_identity() -> None:
    result = execute_canonical_assessment()

    assert result.snapshot.case_id == (
        "VCR-001-CASE-001"
    )

    assert result.summary.case_id == (
        result.snapshot.case_id
    )


def test_service_preserves_canonical_snapshot_identity() -> None:
    result = execute_canonical_assessment()

    assert result.snapshot.snapshot_id == (
        "RCP-001-CASE-001-SNAPSHOT-001"
    )

    assert result.snapshot.snapshot_version == 1

    assert result.summary.snapshot_id == (
        result.snapshot.snapshot_id
    )

    assert result.summary.snapshot_version == (
        result.snapshot.snapshot_version
    )


def test_service_graph_contains_thirty_five_canonical_rules() -> None:
    result = execute_canonical_assessment()

    assert result.provenance_graph.total_rules == 35


def test_service_graph_counts_twenty_three_direct_rules() -> None:
    result = execute_canonical_assessment()

    assert (
        result.provenance_graph.directly_observed_count
        == 23
    )


def test_service_graph_counts_seven_derived_rules() -> None:
    result = execute_canonical_assessment()

    assert result.provenance_graph.derived_count == 7


def test_service_graph_counts_five_evidence_assessed_rules() -> None:
    result = execute_canonical_assessment()

    assert (
        result.provenance_graph.evidence_assessed_count
        == 5
    )


def test_service_graph_reconciles_all_canonical_rule_categories() -> None:
    result = execute_canonical_assessment()

    graph = result.provenance_graph

    assert (
        graph.directly_observed_count
        + graph.derived_count
        + graph.evidence_assessed_count
    ) == graph.total_rules

    assert graph.total_rules == 35


def test_service_summary_contains_thirty_five_comparisons() -> None:
    result = execute_canonical_assessment()

    assert result.summary.total_comparisons == 35

    assert len(
        result.summary.comparisons,
    ) == 35


def test_service_summary_preserves_seventy_observation_identities() -> None:
    result = execute_canonical_assessment()

    observation_ids = {
        observation_id
        for comparison in result.summary.comparisons
        for observation_id in (
            comparison.initial_observation_id,
            comparison.final_observation_id,
        )
    }

    assert len(
        observation_ids,
    ) == 70


def test_service_summary_counts_fourteen_total_improvements() -> None:
    result = execute_canonical_assessment()

    assert result.summary.total_improved_count == 14


def test_service_summary_counts_nine_direct_improvements() -> None:
    result = execute_canonical_assessment()

    assert (
        result.summary.directly_observed_improved_count
        == 9
    )


def test_service_summary_counts_five_derived_improvements() -> None:
    result = execute_canonical_assessment()

    assert result.summary.derived_improved_count == 5


def test_service_summary_counts_sixteen_preserved_conditions() -> None:
    result = execute_canonical_assessment()

    assert result.summary.unchanged_count == 16


def test_service_summary_counts_five_indeterminate_conditions() -> None:
    result = execute_canonical_assessment()

    assert result.summary.indeterminate_count == 5


def test_service_summary_reports_zero_regressions() -> None:
    result = execute_canonical_assessment()

    assert result.summary.regressed_count == 0


def test_service_does_not_count_derived_improvements_as_direct() -> None:
    result = execute_canonical_assessment()

    assert (
        result.summary.directly_observed_improved_count
        + result.summary.derived_improved_count
    ) == result.summary.total_improved_count

    assert (
        result.summary.directly_observed_improved_count
        == 9
    )

    assert (
        result.summary.directly_observed_improved_count
        != result.summary.total_improved_count
    )


def test_service_preserves_geo_005_contextual_policy_dependency() -> None:
    result = execute_canonical_assessment()

    provenance = next(
        record
        for record in result.provenance_graph.records
        if record.rule_id == "GEO-005"
    )

    assert (
        provenance.provenance_type
        is RuleProvenanceType.DERIVED
    )

    assert provenance.source_rule_ids == ()

    assert len(
        provenance.dependency_sources,
    ) == 1

    source = provenance.dependency_sources[0]

    assert source.source_id == (
        "CP01-CONTEXTUAL-ADAPTATION"
    )

    assert (
        source.source_type
        is DependencySourceType.CONTEXT_POLICY
    )


def test_service_does_not_count_context_policy_as_rule() -> None:
    result = execute_canonical_assessment()

    assert result.provenance_graph.context_policy_ids == (
        "CP01-CONTEXTUAL-ADAPTATION",
    )

    assert (
        "CP01-CONTEXTUAL-ADAPTATION"
        not in {
            record.rule_id
            for record
            in result.provenance_graph.records
        }
    )

    assert result.provenance_graph.total_rules == 35


def test_service_preserves_canonical_initial_evidence_identity() -> None:
    result = execute_canonical_assessment()

    conclusive = tuple(
        comparison
        for comparison in result.summary.comparisons
        if (
            comparison.change_status
            is not ObservationChangeStatus.INDETERMINATE
        )
    )

    assert len(
        conclusive,
    ) == 30

    assert {
        comparison.initial_evidence_ids
        for comparison in conclusive
    } == {
        ("ART-003",),
    }


def test_service_preserves_canonical_final_evidence_identity() -> None:
    result = execute_canonical_assessment()

    conclusive = tuple(
        comparison
        for comparison in result.summary.comparisons
        if (
            comparison.change_status
            is not ObservationChangeStatus.INDETERMINATE
        )
    )

    assert {
        comparison.final_evidence_ids
        for comparison in conclusive
    } == {
        ("ART-002",),
    }


def test_service_does_not_invent_evidence_for_indeterminate_rules() -> None:
    result = execute_canonical_assessment()

    indeterminate = tuple(
        comparison
        for comparison in result.summary.comparisons
        if (
            comparison.change_status
            is ObservationChangeStatus.INDETERMINATE
        )
    )

    assert {
        comparison.rule_id
        for comparison in indeterminate
    } == {
        "GEO-004",
        "PHO-002",
        "CAP-001",
        "CAP-003",
        "CAP-004",
    }

    assert all(
        comparison.initial_evidence_ids == ()
        and comparison.final_evidence_ids == ()
        for comparison in indeterminate
    )


def test_service_preserves_human_declared_sears_context() -> None:
    result = execute_canonical_assessment()

    retailer = next(
        dimension
        for dimension in result.snapshot.dimensions
        if (
            dimension.dimension_id
            == "CTX-RETAILER-001"
        )
    )

    assert retailer.value == (
        "SEARS_MEXICO_HUMAN_DECLARED"
    )

    assert (
        retailer.applicability
        is DimensionApplicability.DISPUTED
    )

    assert (
        retailer.evidence_status
        is DimensionEvidenceStatus.DISPUTED
    )

    assert (
        retailer.evidence_status
        is not (
            DimensionEvidenceStatus.INDEPENDENTLY_VERIFIED
        )
    )


def test_service_reconciles_entire_canonical_change_distribution() -> None:
    result = execute_canonical_assessment()

    summary = result.summary

    assert (
        summary.total_improved_count
        + summary.unchanged_count
        + summary.regressed_count
        + summary.indeterminate_count
    ) == summary.total_comparisons

    assert summary.total_comparisons == 35
