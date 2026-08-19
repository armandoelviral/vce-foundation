from dataclasses import dataclass

from sp001.contracts.retail_context_rule_improvement_summary import (
    RuleImprovementSummary,
    summarize_rule_improvements,
)
from sp001.contracts.retail_context_rule_observation_comparison import (
    RuleObservationComparison,
)
from sp001.contracts.retail_context_rule_provenance import (
    RetailContextRuleProvenance,
)
from sp001.contracts.retail_context_rule_provenance_graph import (
    RuleProvenanceGraph,
    build_rule_provenance_graph,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)


@dataclass(frozen=True, slots=True)
class RetailContextAssessmentResult:
    """Immutable result of one customer-scoped retail assessment."""

    snapshot: RetailContextSnapshot
    provenance_graph: RuleProvenanceGraph
    summary: RuleImprovementSummary


def execute_retail_context_assessment(
    *,
    snapshot: RetailContextSnapshot,
    comparisons: tuple[
        RuleObservationComparison,
        ...,
    ],
    provenance_records: tuple[
        RetailContextRuleProvenance,
        ...,
    ],
    context_policy_ids: tuple[str, ...] = (),
) -> RetailContextAssessmentResult:
    """Compose existing retail evidence and provenance contracts."""

    if not isinstance(
        snapshot,
        RetailContextSnapshot,
    ):
        raise TypeError(
            "snapshot must be a "
            "RetailContextSnapshot"
        )

    provenance_graph = build_rule_provenance_graph(
        records=provenance_records,
        context_policy_ids=context_policy_ids,
    )

    summary = summarize_rule_improvements(
        comparisons=comparisons,
        provenance_graph=provenance_graph,
    )

    if summary.case_id != snapshot.case_id:
        raise ValueError(
            "assessment case_id does not match snapshot"
        )

    if (
        summary.snapshot_id
        != snapshot.snapshot_id
    ):
        raise ValueError(
            "assessment snapshot_id does not match snapshot"
        )

    if (
        summary.snapshot_version
        != snapshot.snapshot_version
    ):
        raise ValueError(
            "assessment snapshot_version does not match snapshot"
        )

    comparison_rule_ids = {
        comparison.rule_id
        for comparison in summary.comparisons
    }

    for provenance in provenance_graph.records:
        if provenance.rule_id not in comparison_rule_ids:
            raise ValueError(
                "missing comparison for rule_id: "
                f"{provenance.rule_id}"
            )

    return RetailContextAssessmentResult(
        snapshot=snapshot,
        provenance_graph=provenance_graph,
        summary=summary,
    )
