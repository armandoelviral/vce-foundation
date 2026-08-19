from dataclasses import dataclass

from sp001.contracts.retail_context_rule_observation_comparison import (
    ObservationChangeStatus,
    RuleObservationComparison,
)
from sp001.contracts.retail_context_rule_provenance import (
    RuleProvenanceType,
)
from sp001.contracts.retail_context_rule_provenance_graph import (
    RuleProvenanceGraph,
)


@dataclass(frozen=True, slots=True)
class RuleImprovementSummary:
    """Immutable, provenance-aware summary of retail rule comparisons."""

    case_id: str
    snapshot_id: str
    snapshot_version: int
    comparisons: tuple[RuleObservationComparison, ...]
    total_comparisons: int
    total_improved_count: int
    directly_observed_improved_count: int
    derived_improved_count: int
    unchanged_count: int
    regressed_count: int
    indeterminate_count: int


def summarize_rule_improvements(
    *,
    comparisons: tuple[RuleObservationComparison, ...],
    provenance_graph: RuleProvenanceGraph,
) -> RuleImprovementSummary:
    """Summarize observed changes without inflating derived improvements."""

    if not isinstance(
        provenance_graph,
        RuleProvenanceGraph,
    ):
        raise TypeError(
            "provenance_graph must be a "
            "RuleProvenanceGraph"
        )

    if not isinstance(
        comparisons,
        tuple,
    ):
        raise TypeError(
            "comparisons must be an immutable tuple"
        )

    if not comparisons:
        raise ValueError(
            "comparisons must not be empty"
        )

    provenance_by_id = {
        record.rule_id: record
        for record in provenance_graph.records
    }

    seen_rule_ids: set[str] = set()

    reference_case_id: str | None = None
    reference_snapshot_id: str | None = None
    reference_snapshot_version: int | None = None

    for comparison in comparisons:
        if not isinstance(
            comparison,
            RuleObservationComparison,
        ):
            raise TypeError(
                "every comparison must be a "
                "RuleObservationComparison"
            )

        if comparison.rule_id not in provenance_by_id:
            raise ValueError(
                "missing provenance for rule_id: "
                f"{comparison.rule_id}"
            )

        if comparison.rule_id in seen_rule_ids:
            raise ValueError(
                "duplicate comparison rule_id: "
                f"{comparison.rule_id}"
            )

        seen_rule_ids.add(
            comparison.rule_id
        )

        if reference_case_id is None:
            reference_case_id = (
                comparison.case_id
            )

            reference_snapshot_id = (
                comparison.snapshot_id
            )

            reference_snapshot_version = (
                comparison.snapshot_version
            )

            continue

        if comparison.case_id != reference_case_id:
            raise ValueError(
                "comparison case_id does not match"
            )

        if (
            comparison.snapshot_id
            != reference_snapshot_id
        ):
            raise ValueError(
                "comparison snapshot_id does not match"
            )

        if (
            comparison.snapshot_version
            != reference_snapshot_version
        ):
            raise ValueError(
                "comparison snapshot_version does not match"
            )

    improved_comparisons = tuple(
        comparison
        for comparison in comparisons
        if (
            comparison.change_status
            is ObservationChangeStatus.IMPROVED
        )
    )

    directly_observed_improved_count = sum(
        provenance_by_id[
            comparison.rule_id
        ].provenance_type
        is RuleProvenanceType.DIRECTLY_OBSERVED
        for comparison in improved_comparisons
    )

    derived_improved_count = sum(
        provenance_by_id[
            comparison.rule_id
        ].provenance_type
        is RuleProvenanceType.DERIVED
        for comparison in improved_comparisons
    )

    unchanged_count = sum(
        comparison.change_status
        is ObservationChangeStatus.UNCHANGED
        for comparison in comparisons
    )

    regressed_count = sum(
        comparison.change_status
        is ObservationChangeStatus.REGRESSED
        for comparison in comparisons
    )

    indeterminate_count = sum(
        comparison.change_status
        is ObservationChangeStatus.INDETERMINATE
        for comparison in comparisons
    )

    return RuleImprovementSummary(
        case_id=comparisons[0].case_id,
        snapshot_id=comparisons[0].snapshot_id,
        snapshot_version=(
            comparisons[0].snapshot_version
        ),
        comparisons=comparisons,
        total_comparisons=len(comparisons),
        total_improved_count=len(
            improved_comparisons
        ),
        directly_observed_improved_count=(
            directly_observed_improved_count
        ),
        derived_improved_count=(
            derived_improved_count
        ),
        unchanged_count=unchanged_count,
        regressed_count=regressed_count,
        indeterminate_count=indeterminate_count,
    )
