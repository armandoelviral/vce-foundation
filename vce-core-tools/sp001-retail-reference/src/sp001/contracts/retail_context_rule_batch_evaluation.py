from dataclasses import dataclass

from sp001.contracts.retail_context_rule import (
    RetailContextRule,
)
from sp001.contracts.retail_context_rule_evaluation import (
    RuleEvaluationResult,
    RuleEvaluationStatus,
    evaluate_context_rule,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)


@dataclass(frozen=True, slots=True)
class RuleBatchEvaluationResult:
    """Immutable evaluation results for a customer-defined rule batch."""

    snapshot_id: str
    snapshot_version: int
    case_id: str
    rule_results: tuple[RuleEvaluationResult, ...]
    total_rules: int
    evaluable_count: int
    insufficient_evidence_count: int
    disputed_count: int


def evaluate_context_rule_batch(
    *,
    snapshot: RetailContextSnapshot,
    rules: tuple[RetailContextRule, ...],
) -> RuleBatchEvaluationResult:
    """Evaluate each rule independently against the same retail context."""

    if not isinstance(
        snapshot,
        RetailContextSnapshot,
    ):
        raise TypeError(
            "snapshot must be a RetailContextSnapshot"
        )

    if not isinstance(
        rules,
        tuple,
    ):
        raise TypeError(
            "rules must be an immutable tuple"
        )

    if not rules:
        raise ValueError(
            "rules must not be empty"
        )

    seen_rule_ids: set[str] = set()

    for rule in rules:
        if not isinstance(
            rule,
            RetailContextRule,
        ):
            raise TypeError(
                "every rule must be a RetailContextRule"
            )

        if rule.rule_id in seen_rule_ids:
            raise ValueError(
                "duplicate rule_id: "
                f"{rule.rule_id}"
            )

        seen_rule_ids.add(
            rule.rule_id
        )

    rule_results = tuple(
        evaluate_context_rule(
            snapshot=snapshot,
            rule=rule,
        )
        for rule in rules
    )

    evaluable_count = sum(
        result.status
        is RuleEvaluationStatus.EVALUABLE
        for result in rule_results
    )

    insufficient_evidence_count = sum(
        result.status
        is RuleEvaluationStatus.INSUFFICIENT_EVIDENCE
        for result in rule_results
    )

    disputed_count = sum(
        result.status
        is RuleEvaluationStatus.DISPUTED
        for result in rule_results
    )

    return RuleBatchEvaluationResult(
        snapshot_id=snapshot.snapshot_id,
        snapshot_version=snapshot.snapshot_version,
        case_id=snapshot.case_id,
        rule_results=rule_results,
        total_rules=len(rule_results),
        evaluable_count=evaluable_count,
        insufficient_evidence_count=(
            insufficient_evidence_count
        ),
        disputed_count=disputed_count,
    )
