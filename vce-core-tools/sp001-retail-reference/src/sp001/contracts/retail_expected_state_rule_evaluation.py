from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.retail_context_dimension_evaluation import (
    DimensionEvaluationStatus,
    evaluate_context_dimension,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)
from sp001.contracts.retail_expected_state_rule import (
    RetailExpectedStateRule,
)


class ExpectedStateRuleEvaluationStatus(StrEnum):
    """Evidence-bounded applicability of a customer-declared rule."""

    APPLICABLE = "APPLICABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    DISPUTED = "DISPUTED"


@dataclass(frozen=True, slots=True)
class ExpectedStateRuleEvaluationResult:
    """Immutable rule evaluation without generating an expected state."""

    expected_state_rule_id: str
    expected_state_rule_version: int
    snapshot_id: str
    snapshot_version: int
    context_definition_id: str
    definition_version: int
    status: ExpectedStateRuleEvaluationStatus
    matched_dimension_ids: tuple[str, ...]
    missing_dimension_types: tuple[str, ...]
    insufficient_evidence_dimension_types: tuple[str, ...]
    disputed_dimension_types: tuple[str, ...]
    mismatched_dimension_types: tuple[str, ...]


def evaluate_retail_expected_state_rule(
    *,
    rule: RetailExpectedStateRule,
    snapshot: RetailContextSnapshot,
) -> ExpectedStateRuleEvaluationResult:
    """Evaluate declared conditions without fabricating absent evidence."""

    if not isinstance(
        rule,
        RetailExpectedStateRule,
    ):
        raise TypeError(
            "rule must be a "
            "RetailExpectedStateRule"
        )

    if not isinstance(
        snapshot,
        RetailContextSnapshot,
    ):
        raise TypeError(
            "snapshot must be a "
            "RetailContextSnapshot"
        )

    if snapshot.context_definition is None:
        raise ValueError(
            "snapshot requires "
            "context_definition"
        )

    if snapshot.context_scope is None:
        raise ValueError(
            "snapshot requires "
            "context_scope"
        )

    snapshot_definition = (
        snapshot.context_definition
    )

    rule_definition = (
        rule.context_definition
    )

    if (
        rule_definition.customer_id
        != snapshot_definition.customer_id
    ):
        raise ValueError(
            "rule customer must match "
            "snapshot customer"
        )

    if (
        rule_definition.context_definition_id
        != snapshot_definition.context_definition_id
    ):
        raise ValueError(
            "rule context_definition must match "
            "snapshot context_definition"
        )

    if (
        rule_definition.definition_version
        != snapshot_definition.definition_version
    ):
        raise ValueError(
            "rule definition_version must match "
            "snapshot definition_version"
        )

    dimensions_by_type: dict[
        str,
        list,
    ] = {}

    for dimension in snapshot.dimensions:
        dimensions_by_type.setdefault(
            dimension.dimension_type,
            [],
        ).append(
            dimension,
        )

    matched_dimension_ids: list[str] = []
    missing_dimension_types: list[str] = []
    insufficient_dimension_types: list[str] = []
    disputed_dimension_types: list[str] = []
    mismatched_dimension_types: list[str] = []

    for (
        dimension_type,
        expected_dimension_value,
    ) in rule.required_dimension_values:
        available_dimensions = (
            dimensions_by_type.get(
                dimension_type,
            )
        )

        if not available_dimensions:
            missing_dimension_types.append(
                dimension_type,
            )

            continue

        evaluations = tuple(
            (
                dimension,
                evaluate_context_dimension(
                    dimension,
                ),
            )
            for dimension in available_dimensions
        )

        if any(
            evaluation
            is DimensionEvaluationStatus.DISPUTED
            for (
                dimension,
                evaluation,
            ) in evaluations
        ):
            disputed_dimension_types.append(
                dimension_type,
            )

            continue

        matching_dimensions = tuple(
            dimension
            for (
                dimension,
                evaluation,
            ) in evaluations
            if (
                evaluation
                is DimensionEvaluationStatus.EVALUABLE
                and dimension.value
                == expected_dimension_value
            )
        )

        if matching_dimensions:
            matched_dimension_ids.append(
                matching_dimensions[0].dimension_id,
            )

            continue

        if any(
            evaluation
            is DimensionEvaluationStatus.EVALUABLE
            for (
                dimension,
                evaluation,
            ) in evaluations
        ):
            mismatched_dimension_types.append(
                dimension_type,
            )

            continue

        if all(
            evaluation
            is DimensionEvaluationStatus.NOT_APPLICABLE
            for (
                dimension,
                evaluation,
            ) in evaluations
        ):
            mismatched_dimension_types.append(
                dimension_type,
            )

            continue

        insufficient_dimension_types.append(
            dimension_type,
        )

    if disputed_dimension_types:
        status = (
            ExpectedStateRuleEvaluationStatus.DISPUTED
        )

    elif (
        missing_dimension_types
        or insufficient_dimension_types
    ):
        status = (
            ExpectedStateRuleEvaluationStatus
            .INSUFFICIENT_EVIDENCE
        )

    elif mismatched_dimension_types:
        status = (
            ExpectedStateRuleEvaluationStatus
            .NOT_APPLICABLE
        )

    else:
        status = (
            ExpectedStateRuleEvaluationStatus.APPLICABLE
        )

    return ExpectedStateRuleEvaluationResult(
        expected_state_rule_id=(
            rule.expected_state_rule_id
        ),
        expected_state_rule_version=(
            rule.expected_state_rule_version
        ),
        snapshot_id=snapshot.snapshot_id,
        snapshot_version=snapshot.snapshot_version,
        context_definition_id=(
            snapshot_definition.context_definition_id
        ),
        definition_version=(
            snapshot_definition.definition_version
        ),
        status=status,
        matched_dimension_ids=tuple(
            matched_dimension_ids,
        ),
        missing_dimension_types=tuple(
            missing_dimension_types,
        ),
        insufficient_evidence_dimension_types=tuple(
            insufficient_dimension_types,
        ),
        disputed_dimension_types=tuple(
            disputed_dimension_types,
        ),
        mismatched_dimension_types=tuple(
            mismatched_dimension_types,
        ),
    )
