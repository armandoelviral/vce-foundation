from collections import Counter

from sp001.contracts.retail_context_dependency_source import (
    DependencySourceType,
    RetailContextDependencySource,
)
from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
    RetailContextDimension,
)
from sp001.contracts.retail_context_rule import (
    RetailContextRule,
)
from sp001.contracts.retail_context_rule_evaluation import (
    evaluate_context_rule,
)
from sp001.contracts.retail_context_rule_improvement_summary import (
    summarize_rule_improvements,
)
from sp001.contracts.retail_context_rule_observation import (
    RetailContextRuleObservation,
    RuleObservationStatus,
)
from sp001.contracts.retail_context_rule_observation_binding import (
    bind_rule_observation,
)
from sp001.contracts.retail_context_rule_observation_comparison import (
    ObservationChangeStatus,
    compare_rule_observations,
)
from sp001.contracts.retail_context_rule_provenance import (
    RetailContextRuleProvenance,
    RuleProvenanceType,
)
from sp001.contracts.retail_context_rule_provenance_graph import (
    build_rule_provenance_graph,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)
from sp001.models.objective import Objective


CASE_ID = "VCR-001-CASE-001"

SNAPSHOT_ID = "RCP-001-CASE-001-SNAPSHOT-001"

INITIAL_EVIDENCE_ID = "ART-003"

FINAL_EVIDENCE_ID = "ART-002"

CONTEXT_POLICY_ID = "CP01-CONTEXTUAL-ADAPTATION"


DIRECTLY_OBSERVED_IMPROVED = (
    "CLR-001",
    "CLR-002",
    "CLR-003",
    "CLR-004",
    "CLR-005",
    "PRD-001",
    "PRD-002",
    "LYR-001",
    "LYR-002",
)


DERIVED_IMPROVED = (
    "PRD-003",
    "LYR-003",
    "LYR-004",
    "GEO-001",
    "GEO-002",
)


DIRECTLY_OBSERVED_UNCHANGED = (
    "BRD-001",
    "BRD-002",
    "STR-001",
    "STR-002",
    "STR-003",
    "STR-004",
    "PRD-004",
    "PRD-005",
    "GEO-003",
    "PHO-001",
    "PHO-003",
    "OCC-001",
    "OCC-003",
    "CAP-002",
)


DERIVED_UNCHANGED = (
    "GEO-005",
    "OCC-002",
)


EVIDENCE_ASSESSED = (
    "GEO-004",
    "PHO-002",
    "CAP-001",
    "CAP-003",
    "CAP-004",
)


CANONICAL_RULE_IDS = (
    "BRD-001",
    "BRD-002",
    "STR-001",
    "STR-002",
    "STR-003",
    "STR-004",
    "CLR-001",
    "CLR-002",
    "CLR-003",
    "CLR-004",
    "CLR-005",
    "PRD-001",
    "PRD-002",
    "PRD-003",
    "PRD-004",
    "PRD-005",
    "LYR-001",
    "LYR-002",
    "LYR-003",
    "LYR-004",
    "GEO-001",
    "GEO-002",
    "GEO-003",
    "GEO-004",
    "GEO-005",
    "PHO-001",
    "PHO-002",
    "PHO-003",
    "OCC-001",
    "OCC-002",
    "OCC-003",
    "CAP-001",
    "CAP-002",
    "CAP-003",
    "CAP-004",
)


DERIVED_RULE_SOURCES = {
    "PRD-003": (
        "CLR-001",
        "CLR-002",
        "CLR-003",
        "CLR-004",
        "PRD-001",
        "PRD-002",
        "LYR-001",
        "LYR-002",
    ),
    "LYR-003": (
        "LYR-001",
        "LYR-002",
    ),
    "LYR-004": (
        "LYR-001",
        "LYR-002",
        "PRD-003",
    ),
    "GEO-001": (
        "CLR-001",
        "CLR-002",
        "CLR-003",
        "CLR-004",
        "CLR-005",
    ),
    "GEO-002": (
        "PRD-001",
        "PRD-002",
        "LYR-001",
        "LYR-002",
    ),
    "OCC-002": (
        "LYR-001",
        "LYR-002",
        "OCC-001",
    ),
}


def create_case():
    objective = Objective(
        objective_id="VCR-001-OBJECTIVE-001",
        title=(
            "Verify customer-declared "
            "retail fixture presentation"
        ),
        description=(
            "Evaluate visual merchandising evidence "
            "without inferring acceptance or revenue."
        ),
    )

    return objective.create_case(
        case_id=CASE_ID,
        scope="SEARS-MEXICO-HUMAN-DECLARED",
    )


def create_snapshot(
    case_id: str,
) -> RetailContextSnapshot:
    fixture = RetailContextDimension(
        dimension_id="CTX-FIXTURE-001",
        dimension_type="FIXTURE_TYPE",
        applicability=(
            DimensionApplicability.REQUIRED
        ),
        evidence_status=(
            DimensionEvidenceStatus.DOCUMENTED
        ),
        value="TCP_PRESENTATION_FIXTURE",
    )

    retailer = RetailContextDimension(
        dimension_id="CTX-RETAILER-001",
        dimension_type="RETAILER_CONTEXT",
        applicability=(
            DimensionApplicability.DISPUTED
        ),
        evidence_status=(
            DimensionEvidenceStatus.DISPUTED
        ),
        value="SEARS_MEXICO_HUMAN_DECLARED",
    )

    return RetailContextSnapshot(
        snapshot_id=SNAPSHOT_ID,
        snapshot_version=1,
        case_id=case_id,
        dimensions=(
            fixture,
            retailer,
        ),
    )


def create_rule(
    rule_id: str,
) -> RetailContextRule:
    return RetailContextRule(
        rule_id=rule_id,
        rule_type=(
            "CUSTOMER_DECLARED_RETAIL_CONSTRAINT"
        ),
        required_dimension_ids=(
            "CTX-FIXTURE-001",
        ),
    )


def create_observation(
    *,
    rule_id: str,
    snapshot: RetailContextSnapshot,
    phase: str,
    status: RuleObservationStatus,
) -> RetailContextRuleObservation:
    evidence_ids = ()

    if status in {
        RuleObservationStatus.CONFORMANT,
        RuleObservationStatus.NON_CONFORMANT,
    }:
        evidence_ids = (
            INITIAL_EVIDENCE_ID
            if phase == "OBS"
            else FINAL_EVIDENCE_ID,
        )

    return RetailContextRuleObservation(
        observation_id=(
            f"{CASE_ID}-{rule_id}-{phase}"
        ),
        rule_id=rule_id,
        snapshot_id=snapshot.snapshot_id,
        snapshot_version=snapshot.snapshot_version,
        case_id=snapshot.case_id,
        status=status,
        evidence_ids=evidence_ids,
    )


def observation_statuses(
    rule_id: str,
) -> tuple[
    RuleObservationStatus,
    RuleObservationStatus,
]:
    if rule_id in (
        DIRECTLY_OBSERVED_IMPROVED
        + DERIVED_IMPROVED
    ):
        return (
            RuleObservationStatus.NON_CONFORMANT,
            RuleObservationStatus.CONFORMANT,
        )

    if rule_id in (
        DIRECTLY_OBSERVED_UNCHANGED
        + DERIVED_UNCHANGED
    ):
        return (
            RuleObservationStatus.CONFORMANT,
            RuleObservationStatus.CONFORMANT,
        )

    if rule_id in EVIDENCE_ASSESSED:
        return (
            RuleObservationStatus.INSUFFICIENT_EVIDENCE,
            RuleObservationStatus.INSUFFICIENT_EVIDENCE,
        )

    raise ValueError(
        f"unknown canonical rule_id: {rule_id}"
    )


def create_comparison(
    *,
    rule_id: str,
    snapshot: RetailContextSnapshot,
):
    rule = create_rule(
        rule_id,
    )

    evaluation = evaluate_context_rule(
        snapshot=snapshot,
        rule=rule,
    )

    initial_status, final_status = (
        observation_statuses(
            rule_id,
        )
    )

    initial = bind_rule_observation(
        evaluation=evaluation,
        observation=create_observation(
            rule_id=rule_id,
            snapshot=snapshot,
            phase="OBS",
            status=initial_status,
        ),
    )

    final = bind_rule_observation(
        evaluation=evaluation,
        observation=create_observation(
            rule_id=rule_id,
            snapshot=snapshot,
            phase="OUT",
            status=final_status,
        ),
    )

    return compare_rule_observations(
        initial=initial,
        final=final,
    )


def create_provenance(
    rule_id: str,
) -> RetailContextRuleProvenance:
    if rule_id in EVIDENCE_ASSESSED:
        return RetailContextRuleProvenance(
            rule_id=rule_id,
            provenance_type=(
                RuleProvenanceType.EVIDENCE_ASSESSED
            ),
        )

    if rule_id == "GEO-005":
        return RetailContextRuleProvenance(
            rule_id=rule_id,
            provenance_type=(
                RuleProvenanceType.DERIVED
            ),
            dependency_sources=(
                RetailContextDependencySource(
                    source_id=CONTEXT_POLICY_ID,
                    source_type=(
                        DependencySourceType.CONTEXT_POLICY
                    ),
                ),
            ),
        )

    if rule_id in DERIVED_RULE_SOURCES:
        return RetailContextRuleProvenance(
            rule_id=rule_id,
            provenance_type=(
                RuleProvenanceType.DERIVED
            ),
            dependency_sources=tuple(
                RetailContextDependencySource(
                    source_id=source_rule_id,
                    source_type=(
                        DependencySourceType.RULE
                    ),
                )
                for source_rule_id
                in DERIVED_RULE_SOURCES[rule_id]
            ),
        )

    return RetailContextRuleProvenance(
        rule_id=rule_id,
        provenance_type=(
            RuleProvenanceType.DIRECTLY_OBSERVED
        ),
    )


def create_canonical_graph():
    return build_rule_provenance_graph(
        records=tuple(
            create_provenance(
                rule_id,
            )
            for rule_id in CANONICAL_RULE_IDS
        ),
        context_policy_ids=(
            CONTEXT_POLICY_ID,
        ),
    )


def create_canonical_comparisons():
    case = create_case()

    snapshot = create_snapshot(
        case.case_id,
    )

    return tuple(
        create_comparison(
            rule_id=rule_id,
            snapshot=snapshot,
        )
        for rule_id in CANONICAL_RULE_IDS
    )


def create_canonical_summary():
    return summarize_rule_improvements(
        comparisons=(
            create_canonical_comparisons()
        ),
        provenance_graph=(
            create_canonical_graph()
        ),
    )


def test_canonical_matrix_contains_exactly_thirty_five_rules() -> None:
    assert len(CANONICAL_RULE_IDS) == 35

    assert len(
        set(CANONICAL_RULE_IDS),
    ) == 35


def test_canonical_matrix_preserves_nine_constraint_families() -> None:
    families = Counter(
        rule_id.split("-")[0]
        for rule_id in CANONICAL_RULE_IDS
    )

    assert dict(families) == {
        "BRD": 2,
        "STR": 4,
        "CLR": 5,
        "PRD": 5,
        "LYR": 4,
        "GEO": 5,
        "PHO": 3,
        "OCC": 3,
        "CAP": 4,
    }


def test_canonical_graph_contains_thirty_five_rules() -> None:
    graph = create_canonical_graph()

    assert graph.total_rules == 35


def test_canonical_graph_counts_twenty_three_direct_observations() -> None:
    graph = create_canonical_graph()

    assert graph.directly_observed_count == 23


def test_canonical_graph_counts_seven_derived_rules() -> None:
    graph = create_canonical_graph()

    assert graph.derived_count == 7


def test_canonical_graph_counts_five_evidence_assessments() -> None:
    graph = create_canonical_graph()

    assert graph.evidence_assessed_count == 5


def test_canonical_graph_reconciles_all_provenance_categories() -> None:
    graph = create_canonical_graph()

    assert (
        graph.directly_observed_count
        + graph.derived_count
        + graph.evidence_assessed_count
    ) == 35


def test_canonical_graph_preserves_exact_derived_rule_set() -> None:
    graph = create_canonical_graph()

    derived_rule_ids = {
        record.rule_id
        for record in graph.records
        if (
            record.provenance_type
            is RuleProvenanceType.DERIVED
        )
    }

    assert derived_rule_ids == {
        "PRD-003",
        "LYR-003",
        "LYR-004",
        "GEO-001",
        "GEO-002",
        "GEO-005",
        "OCC-002",
    }


def test_geo_005_depends_on_context_policy_not_invented_rule() -> None:
    graph = create_canonical_graph()

    provenance = next(
        record
        for record in graph.records
        if record.rule_id == "GEO-005"
    )

    assert provenance.source_rule_ids == ()

    assert len(
        provenance.dependency_sources,
    ) == 1

    source = provenance.dependency_sources[0]

    assert source.source_id == CONTEXT_POLICY_ID

    assert (
        source.source_type
        is DependencySourceType.CONTEXT_POLICY
    )

    assert CONTEXT_POLICY_ID not in {
        record.rule_id
        for record in graph.records
    }


def test_occ_002_preserves_layering_and_occlusion_sources() -> None:
    graph = create_canonical_graph()

    provenance = next(
        record
        for record in graph.records
        if record.rule_id == "OCC-002"
    )

    assert tuple(
        source.source_id
        for source in provenance.dependency_sources
    ) == (
        "LYR-001",
        "LYR-002",
        "OCC-001",
    )


def test_canonical_case_produces_thirty_five_comparisons() -> None:
    comparisons = create_canonical_comparisons()

    assert len(comparisons) == 35


def test_canonical_case_produces_seventy_observation_identities() -> None:
    comparisons = create_canonical_comparisons()

    observation_ids = {
        observation_id
        for comparison in comparisons
        for observation_id in (
            comparison.initial_observation_id,
            comparison.final_observation_id,
        )
    }

    assert len(observation_ids) == 70


def test_canonical_summary_counts_fourteen_total_improvements() -> None:
    summary = create_canonical_summary()

    assert summary.total_comparisons == 35
    assert summary.total_improved_count == 14


def test_canonical_summary_counts_nine_direct_improvements() -> None:
    summary = create_canonical_summary()

    assert summary.directly_observed_improved_count == 9


def test_canonical_summary_counts_five_derived_improvements() -> None:
    summary = create_canonical_summary()

    assert summary.derived_improved_count == 5


def test_canonical_summary_counts_sixteen_unchanged_rules() -> None:
    summary = create_canonical_summary()

    assert summary.unchanged_count == 16


def test_canonical_summary_counts_five_indeterminate_rules() -> None:
    summary = create_canonical_summary()

    assert summary.indeterminate_count == 5


def test_canonical_summary_reports_zero_regressions() -> None:
    summary = create_canonical_summary()

    assert summary.regressed_count == 0


def test_canonical_summary_does_not_inflate_derived_improvements() -> None:
    summary = create_canonical_summary()

    assert (
        summary.directly_observed_improved_count
        + summary.derived_improved_count
    ) == summary.total_improved_count

    assert summary.directly_observed_improved_count == 9

    assert summary.directly_observed_improved_count != (
        summary.total_improved_count
    )


def test_conclusive_observations_use_correct_external_artifact_ids() -> None:
    comparisons = create_canonical_comparisons()

    conclusive = tuple(
        comparison
        for comparison in comparisons
        if (
            comparison.change_status
            is not ObservationChangeStatus.INDETERMINATE
        )
    )

    assert len(conclusive) == 30

    assert {
        comparison.initial_evidence_ids
        for comparison in conclusive
    } == {
        (INITIAL_EVIDENCE_ID,),
    }

    assert {
        comparison.final_evidence_ids
        for comparison in conclusive
    } == {
        (FINAL_EVIDENCE_ID,),
    }


def test_indeterminate_rules_do_not_invent_evidence() -> None:
    comparisons = create_canonical_comparisons()

    indeterminate = tuple(
        comparison
        for comparison in comparisons
        if (
            comparison.change_status
            is ObservationChangeStatus.INDETERMINATE
        )
    )

    assert {
        comparison.rule_id
        for comparison in indeterminate
    } == set(
        EVIDENCE_ASSESSED,
    )

    assert all(
        comparison.initial_evidence_ids == ()
        and comparison.final_evidence_ids == ()
        for comparison in indeterminate
    )


def test_retailer_context_remains_disputed_and_human_declared() -> None:
    case = create_case()

    snapshot = create_snapshot(
        case.case_id,
    )

    retailer = next(
        dimension
        for dimension in snapshot.dimensions
        if (
            dimension.dimension_id
            == "CTX-RETAILER-001"
        )
    )

    assert (
        retailer.value
        == "SEARS_MEXICO_HUMAN_DECLARED"
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


def test_context_policy_is_not_counted_as_canonical_rule() -> None:
    graph = create_canonical_graph()

    assert graph.context_policy_ids == (
        CONTEXT_POLICY_ID,
    )

    assert graph.total_rules == 35

    assert CONTEXT_POLICY_ID not in CANONICAL_RULE_IDS


def test_summary_preserves_case_and_snapshot_identity() -> None:
    summary = create_canonical_summary()

    assert summary.case_id == CASE_ID
    assert summary.snapshot_id == SNAPSHOT_ID
    assert summary.snapshot_version == 1


def test_canonical_change_distribution_reconciles_thirty_five_rules() -> None:
    summary = create_canonical_summary()

    assert (
        summary.total_improved_count
        + summary.unchanged_count
        + summary.regressed_count
        + summary.indeterminate_count
    ) == summary.total_comparisons

    assert summary.total_comparisons == 35
