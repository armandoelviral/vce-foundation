from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.retail_context_dimension_evaluation import (
    DimensionEvaluationStatus,
)
from sp001.contracts.retail_context_rule import (
    RetailContextRule,
)
from sp001.contracts.retail_context_scoped_evaluation import (
    ScopedEvaluationStatus,
    evaluate_context_scope,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)


class RuleEvaluationStatus(StrEnum):
    """Context availability for evaluating a retail commercial rule."""

    EVALUABLE = "EVALUABLE"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    DISPUTED = "DISPUTED"


@dataclass(frozen=True, slots=True)
class RuleEvaluationResult:
    """Immutable contextual evaluation for one identified retail rule."""

    rule_id: str
    rule_type: str
    snapshot_id: str
    snapshot_version: int
    case_id: str
    status: RuleEvaluationStatus
    dimension_results: tuple[
        tuple[str, DimensionEvaluationStatus],
        ...,
    ]
    missing_dimension_ids: tuple[str, ...]


def evaluate_context_rule(
    *,
    snapshot: RetailContextSnapshot,
    rule: RetailContextRule,
) -> RuleEvaluationResult:
    """Determine whether the declared retail rule can be evaluated."""

    if not isinstance(
        snapshot,
        RetailContextSnapshot,
    ):
        raise TypeError(
            "snapshot must be a RetailContextSnapshot"
        )

    if not isinstance(
        rule,
        RetailContextRule,
    ):
        raise TypeError(
            "rule must be a RetailContextRule"
        )

    scoped_result = evaluate_context_scope(
        snapshot,
        required_dimension_ids=(
            rule.required_dimension_ids
        ),
    )

    status_mapping = {
        ScopedEvaluationStatus.EVALUABLE: (
            RuleEvaluationStatus.EVALUABLE
        ),
        ScopedEvaluationStatus.INSUFFICIENT_EVIDENCE: (
            RuleEvaluationStatus.INSUFFICIENT_EVIDENCE
        ),
        ScopedEvaluationStatus.DISPUTED: (
            RuleEvaluationStatus.DISPUTED
        ),
    }

    return RuleEvaluationResult(
        rule_id=rule.rule_id,
        rule_type=rule.rule_type,
        snapshot_id=scoped_result.snapshot_id,
        snapshot_version=scoped_result.snapshot_version,
        case_id=scoped_result.case_id,
        status=status_mapping[
            scoped_result.status
        ],
        dimension_results=(
            scoped_result.dimension_results
        ),
        missing_dimension_ids=(
            scoped_result.missing_dimension_ids
        ),
    )
