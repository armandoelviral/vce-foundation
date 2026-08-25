from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)
from sp001.contracts.retail_expected_state import (
    RetailExpectedState,
)
from sp001.contracts.retail_expected_state_rule import (
    RetailExpectedStateRule,
)
from sp001.contracts.retail_expected_state_rule_evaluation import (
    ExpectedStateRuleEvaluationStatus,
    evaluate_retail_expected_state_rule,
)


def generate_retail_expected_state(
    *,
    expected_state_id: str,
    expected_state_version: int,
    rule: RetailExpectedStateRule,
    snapshot: RetailContextSnapshot,
) -> RetailExpectedState:
    """Generate declared expectations only from applicable retail evidence."""

    evaluation = (
        evaluate_retail_expected_state_rule(
            rule=rule,
            snapshot=snapshot,
        )
    )

    if (
        evaluation.status
        is not ExpectedStateRuleEvaluationStatus.APPLICABLE
    ):
        raise ValueError(
            "expected state requires "
            "an applicable rule: "
            f"{evaluation.status.value}"
        )

    return RetailExpectedState(
        expected_state_id=expected_state_id,
        expected_state_version=expected_state_version,
        snapshot=snapshot,
        expectation_type=rule.expectation_type,
        expected_value=rule.expected_value,
        source_dimension_ids=(
            evaluation.matched_dimension_ids
        ),
        source_policy_ids=(
            rule.source_policy_ids
        ),
    )
