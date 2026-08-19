from dataclasses import dataclass

from sp001.contracts.retail_context_dimension import (
    DimensionApplicability,
    DimensionEvidenceStatus,
)
from sp001.contracts.retail_context_rule_observation import (
    RuleObservationStatus,
)
from sp001.contracts.retail_context_rule_observation_comparison import (
    ObservationChangeStatus,
)
from sp001.contracts.retail_context_rule_provenance import (
    RuleProvenanceType,
)
from sp001.services.retail_context_assessment import (
    RetailContextAssessmentResult,
)


@dataclass(frozen=True, slots=True)
class RetailContextAssessmentRuleReport:
    """Sanitized evidence-backed result for one retail rule."""

    rule_id: str
    initial_status: RuleObservationStatus
    final_status: RuleObservationStatus
    change_status: ObservationChangeStatus
    provenance_type: RuleProvenanceType
    initial_evidence_ids: tuple[str, ...]
    final_evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RetailContextAssessmentReport:
    """Immutable, sanitized projection of one retail assessment."""

    case_id: str
    snapshot_id: str
    snapshot_version: int
    rules: tuple[
        RetailContextAssessmentRuleReport,
        ...,
    ]
    total_rules: int
    directly_observed_count: int
    derived_count: int
    evidence_assessed_count: int
    total_improved_count: int
    directly_observed_improved_count: int
    derived_improved_count: int
    unchanged_count: int
    regressed_count: int
    indeterminate_count: int
    evidence_ids: tuple[str, ...]
    disputed_dimension_ids: tuple[str, ...]
    context_policy_ids: tuple[str, ...]
    customer_acceptance_status: str
    commercial_impact_status: str
    independent_intervention_status: str


def build_retail_context_assessment_report(
    *,
    result: RetailContextAssessmentResult,
) -> RetailContextAssessmentReport:
    """Project assessment evidence without inferring commercial claims."""

    if not isinstance(
        result,
        RetailContextAssessmentResult,
    ):
        raise TypeError(
            "result must be a "
            "RetailContextAssessmentResult"
        )

    provenance_by_rule_id = {
        record.rule_id: record
        for record in result.provenance_graph.records
    }

    rules = tuple(
        RetailContextAssessmentRuleReport(
            rule_id=comparison.rule_id,
            initial_status=comparison.initial_status,
            final_status=comparison.final_status,
            change_status=comparison.change_status,
            provenance_type=(
                provenance_by_rule_id[
                    comparison.rule_id
                ].provenance_type
            ),
            initial_evidence_ids=(
                comparison.initial_evidence_ids
            ),
            final_evidence_ids=(
                comparison.final_evidence_ids
            ),
        )
        for comparison
        in result.summary.comparisons
    )

    evidence_ids = tuple(
        sorted(
            {
                evidence_id
                for rule in rules
                for evidence_id in (
                    rule.initial_evidence_ids
                    + rule.final_evidence_ids
                )
            }
        )
    )

    disputed_dimension_ids = tuple(
        dimension.dimension_id
        for dimension
        in result.snapshot.dimensions
        if (
            dimension.applicability
            is DimensionApplicability.DISPUTED
            or dimension.evidence_status
            is DimensionEvidenceStatus.DISPUTED
        )
    )

    return RetailContextAssessmentReport(
        case_id=result.snapshot.case_id,
        snapshot_id=result.snapshot.snapshot_id,
        snapshot_version=(
            result.snapshot.snapshot_version
        ),
        rules=rules,
        total_rules=(
            result.provenance_graph.total_rules
        ),
        directly_observed_count=(
            result.provenance_graph.directly_observed_count
        ),
        derived_count=(
            result.provenance_graph.derived_count
        ),
        evidence_assessed_count=(
            result.provenance_graph.evidence_assessed_count
        ),
        total_improved_count=(
            result.summary.total_improved_count
        ),
        directly_observed_improved_count=(
            result.summary.directly_observed_improved_count
        ),
        derived_improved_count=(
            result.summary.derived_improved_count
        ),
        unchanged_count=(
            result.summary.unchanged_count
        ),
        regressed_count=(
            result.summary.regressed_count
        ),
        indeterminate_count=(
            result.summary.indeterminate_count
        ),
        evidence_ids=evidence_ids,
        disputed_dimension_ids=(
            disputed_dimension_ids
        ),
        context_policy_ids=(
            result.provenance_graph.context_policy_ids
        ),
        customer_acceptance_status=(
            "NOT_ESTABLISHED"
        ),
        commercial_impact_status=(
            "NOT_ESTABLISHED"
        ),
        independent_intervention_status=(
            "NOT_ESTABLISHED"
        ),
    )
