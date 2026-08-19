from dataclasses import FrozenInstanceError

import pytest

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


def build_snapshot(
    *,
    case_id: str = "CASE-001",
    snapshot_id: str = "RCP-SNAPSHOT-001",
    snapshot_version: int = 1,
) -> RetailContextSnapshot:
    dimension = RetailContextDimension(
        dimension_id="CTX-FIXTURE-001",
        dimension_type="FIXTURE_TYPE",
        applicability=DimensionApplicability.REQUIRED,
        evidence_status=DimensionEvidenceStatus.DOCUMENTED,
        value="BACKWALL",
    )

    return RetailContextSnapshot(
        snapshot_id=snapshot_id,
        snapshot_version=snapshot_version,
        case_id=case_id,
        dimensions=(dimension,),
    )


def build_comparison(
    *,
    rule_id: str,
    initial_status: RuleObservationStatus,
    final_status: RuleObservationStatus,
    case_id: str = "CASE-001",
    snapshot_id: str = "RCP-SNAPSHOT-001",
    snapshot_version: int = 1,
):
    snapshot = build_snapshot(
        case_id=case_id,
        snapshot_id=snapshot_id,
        snapshot_version=snapshot_version,
    )

    rule = RetailContextRule(
        rule_id=rule_id,
        rule_type="CUSTOMER_DEFINED_RULE",
        required_dimension_ids=(
            "CTX-FIXTURE-001",
        ),
    )

    evaluation = evaluate_context_rule(
        snapshot=snapshot,
        rule=rule,
    )

    def observation(
        phase: str,
        status: RuleObservationStatus,
    ) -> RetailContextRuleObservation:
        evidence_ids = ()

        if status in {
            RuleObservationStatus.CONFORMANT,
            RuleObservationStatus.NON_CONFORMANT,
        }:
            evidence_ids = (
                f"ART-{phase}",
            )

        return RetailContextRuleObservation(
            observation_id=f"{rule_id}-{phase}",
            rule_id=rule_id,
            snapshot_id=snapshot.snapshot_id,
            snapshot_version=snapshot.snapshot_version,
            case_id=snapshot.case_id,
            status=status,
            evidence_ids=evidence_ids,
        )

    initial = bind_rule_observation(
        evaluation=evaluation,
        observation=observation(
            "INITIAL",
            initial_status,
        ),
    )

    final = bind_rule_observation(
        evaluation=evaluation,
        observation=observation(
            "FINAL",
            final_status,
        ),
    )

    return compare_rule_observations(
        initial=initial,
        final=final,
    )


def direct(
    rule_id: str,
) -> RetailContextRuleProvenance:
    return RetailContextRuleProvenance(
        rule_id=rule_id,
        provenance_type=(
            RuleProvenanceType.DIRECTLY_OBSERVED
        ),
    )


def derived(
    rule_id: str,
    *source_rule_ids: str,
) -> RetailContextRuleProvenance:
    return RetailContextRuleProvenance(
        rule_id=rule_id,
        provenance_type=(
            RuleProvenanceType.DERIVED
        ),
        source_rule_ids=source_rule_ids,
    )


def improved(
    rule_id: str,
):
    return build_comparison(
        rule_id=rule_id,
        initial_status=(
            RuleObservationStatus.NON_CONFORMANT
        ),
        final_status=(
            RuleObservationStatus.CONFORMANT
        ),
    )


def unchanged(
    rule_id: str,
):
    return build_comparison(
        rule_id=rule_id,
        initial_status=(
            RuleObservationStatus.CONFORMANT
        ),
        final_status=(
            RuleObservationStatus.CONFORMANT
        ),
    )


def test_summary_counts_directly_observed_improvement() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
        ),
    )

    result = summarize_rule_improvements(
        comparisons=(
            improved("RULE-CLR-001"),
        ),
        provenance_graph=graph,
    )

    assert result.total_comparisons == 1
    assert result.total_improved_count == 1
    assert result.directly_observed_improved_count == 1
    assert result.derived_improved_count == 0


def test_summary_separates_direct_and_derived_improvements() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
            derived(
                "RULE-PRD-003",
                "RULE-CLR-001",
            ),
        ),
    )

    result = summarize_rule_improvements(
        comparisons=(
            improved("RULE-CLR-001"),
            improved("RULE-PRD-003"),
        ),
        provenance_graph=graph,
    )

    assert result.total_improved_count == 2
    assert result.directly_observed_improved_count == 1
    assert result.derived_improved_count == 1


def test_summary_counts_unchanged_comparisons() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-BRD-001"),
        ),
    )

    result = summarize_rule_improvements(
        comparisons=(
            unchanged("RULE-BRD-001"),
        ),
        provenance_graph=graph,
    )

    assert result.unchanged_count == 1
    assert result.total_improved_count == 0


def test_summary_counts_regressed_comparisons() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
        ),
    )

    comparison = build_comparison(
        rule_id="RULE-CLR-001",
        initial_status=(
            RuleObservationStatus.CONFORMANT
        ),
        final_status=(
            RuleObservationStatus.NON_CONFORMANT
        ),
    )

    result = summarize_rule_improvements(
        comparisons=(comparison,),
        provenance_graph=graph,
    )

    assert result.regressed_count == 1
    assert result.total_improved_count == 0


def test_summary_counts_indeterminate_comparisons() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-GEO-004"),
        ),
    )

    comparison = build_comparison(
        rule_id="RULE-GEO-004",
        initial_status=(
            RuleObservationStatus.INSUFFICIENT_EVIDENCE
        ),
        final_status=(
            RuleObservationStatus.CONFORMANT
        ),
    )

    result = summarize_rule_improvements(
        comparisons=(comparison,),
        provenance_graph=graph,
    )

    assert result.indeterminate_count == 1
    assert result.total_improved_count == 0


def test_summary_preserves_case_and_snapshot_identity() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
        ),
    )

    result = summarize_rule_improvements(
        comparisons=(
            improved("RULE-CLR-001"),
        ),
        provenance_graph=graph,
    )

    assert result.case_id == "CASE-001"
    assert result.snapshot_id == "RCP-SNAPSHOT-001"
    assert result.snapshot_version == 1


def test_summary_preserves_comparison_order() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
            direct("RULE-CLR-002"),
        ),
    )

    result = summarize_rule_improvements(
        comparisons=(
            improved("RULE-CLR-002"),
            improved("RULE-CLR-001"),
        ),
        provenance_graph=graph,
    )

    assert tuple(
        comparison.rule_id
        for comparison in result.comparisons
    ) == (
        "RULE-CLR-002",
        "RULE-CLR-001",
    )


def test_summary_rejects_invalid_provenance_graph() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "provenance_graph must be a "
            "RuleProvenanceGraph"
        ),
    ):
        summarize_rule_improvements(
            comparisons=(
                improved("RULE-CLR-001"),
            ),
            provenance_graph="GRAPH-001",
        )


def test_summary_rejects_mutable_comparison_collection() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
        ),
    )

    with pytest.raises(
        TypeError,
        match=(
            "comparisons must be an immutable tuple"
        ),
    ):
        summarize_rule_improvements(
            comparisons=[
                improved("RULE-CLR-001"),
            ],
            provenance_graph=graph,
        )


def test_summary_rejects_empty_comparison_collection() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
        ),
    )

    with pytest.raises(
        ValueError,
        match="comparisons must not be empty",
    ):
        summarize_rule_improvements(
            comparisons=(),
            provenance_graph=graph,
        )


def test_summary_rejects_invalid_comparison_element() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
        ),
    )

    with pytest.raises(
        TypeError,
        match=(
            "every comparison must be a "
            "RuleObservationComparison"
        ),
    ):
        summarize_rule_improvements(
            comparisons=(
                "RULE-CLR-001",
            ),
            provenance_graph=graph,
        )


def test_summary_rejects_missing_rule_provenance() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "missing provenance for rule_id: "
            "RULE-PRD-003"
        ),
    ):
        summarize_rule_improvements(
            comparisons=(
                improved("RULE-PRD-003"),
            ),
            provenance_graph=graph,
        )


def test_summary_rejects_duplicate_comparison_rule() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "duplicate comparison rule_id: "
            "RULE-CLR-001"
        ),
    ):
        summarize_rule_improvements(
            comparisons=(
                improved("RULE-CLR-001"),
                improved("RULE-CLR-001"),
            ),
            provenance_graph=graph,
        )


@pytest.mark.parametrize(
    ("field", "invalid_value", "message"),
    (
        (
            "case_id",
            "CASE-002",
            "comparison case_id does not match",
        ),
        (
            "snapshot_id",
            "RCP-SNAPSHOT-002",
            "comparison snapshot_id does not match",
        ),
        (
            "snapshot_version",
            2,
            "comparison snapshot_version does not match",
        ),
    ),
)
def test_summary_rejects_mixed_context_identity(
    field: str,
    invalid_value: str | int,
    message: str,
) -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
            direct("RULE-CLR-002"),
        ),
    )

    first = improved(
        "RULE-CLR-001"
    )

    second = build_comparison(
        rule_id="RULE-CLR-002",
        initial_status=(
            RuleObservationStatus.NON_CONFORMANT
        ),
        final_status=(
            RuleObservationStatus.CONFORMANT
        ),
        **{
            field: invalid_value,
        },
    )

    with pytest.raises(
        ValueError,
        match=message,
    ):
        summarize_rule_improvements(
            comparisons=(
                first,
                second,
            ),
            provenance_graph=graph,
        )


def test_summary_result_is_immutable() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
        ),
    )

    result = summarize_rule_improvements(
        comparisons=(
            improved("RULE-CLR-001"),
        ),
        provenance_graph=graph,
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        result.total_improved_count = 2


def test_summary_does_not_claim_operational_independence() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
            derived(
                "RULE-PRD-003",
                "RULE-CLR-001",
            ),
        ),
    )

    result = summarize_rule_improvements(
        comparisons=(
            improved("RULE-CLR-001"),
            improved("RULE-PRD-003"),
        ),
        provenance_graph=graph,
    )

    assert not hasattr(
        result,
        "independent_interventions",
    )

    assert not hasattr(
        result,
        "customer_accepted",
    )

    assert not hasattr(
        result,
        "commercial_revenue",
    )


def test_summary_change_counts_reconcile_to_total() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
            direct("RULE-BRD-001"),
            direct("RULE-GEO-004"),
        ),
    )

    improved_rule = improved(
        "RULE-CLR-001"
    )

    unchanged_rule = unchanged(
        "RULE-BRD-001"
    )

    indeterminate_rule = build_comparison(
        rule_id="RULE-GEO-004",
        initial_status=(
            RuleObservationStatus.INSUFFICIENT_EVIDENCE
        ),
        final_status=(
            RuleObservationStatus.CONFORMANT
        ),
    )

    result = summarize_rule_improvements(
        comparisons=(
            improved_rule,
            unchanged_rule,
            indeterminate_rule,
        ),
        provenance_graph=graph,
    )

    assert result.total_comparisons == (
        result.total_improved_count
        + result.unchanged_count
        + result.regressed_count
        + result.indeterminate_count
    )
