from dataclasses import dataclass

from sp001.contracts.retail_context_dimension_evaluation import (
    DimensionEvaluationStatus,
)
from sp001.contracts.retail_context_rule_evaluation import (
    RuleEvaluationResult,
    RuleEvaluationStatus,
)
from sp001.contracts.retail_context_rule_observation import (
    RetailContextRuleObservation,
    RuleObservationStatus,
)


@dataclass(frozen=True, slots=True)
class RuleObservationBinding:
    """Immutable association between a rule evaluation and observation."""

    observation_id: str
    rule_id: str
    rule_type: str
    snapshot_id: str
    snapshot_version: int
    case_id: str
    evaluation_status: RuleEvaluationStatus
    observation_status: RuleObservationStatus
    dimension_results: tuple[
        tuple[str, DimensionEvaluationStatus],
        ...,
    ]
    evidence_ids: tuple[str, ...]


def bind_rule_observation(
    *,
    evaluation: RuleEvaluationResult,
    observation: RetailContextRuleObservation,
) -> RuleObservationBinding:
    """Bind one observation to its corresponding contextual evaluation."""

    if not isinstance(
        evaluation,
        RuleEvaluationResult,
    ):
        raise TypeError(
            "evaluation must be a RuleEvaluationResult"
        )

    if not isinstance(
        observation,
        RetailContextRuleObservation,
    ):
        raise TypeError(
            "observation must be a "
            "RetailContextRuleObservation"
        )

    identity_fields = (
        "rule_id",
        "snapshot_id",
        "snapshot_version",
        "case_id",
    )

    for field in identity_fields:
        if (
            getattr(observation, field)
            != getattr(evaluation, field)
        ):
            raise ValueError(
                f"observation {field} "
                "does not match evaluation"
            )

    if (
        evaluation.status
        is RuleEvaluationStatus.INSUFFICIENT_EVIDENCE
        and observation.status
        is not RuleObservationStatus.INSUFFICIENT_EVIDENCE
    ):
        raise ValueError(
            "insufficient evaluation only permits "
            "INSUFFICIENT_EVIDENCE observation"
        )

    if (
        evaluation.status
        is RuleEvaluationStatus.DISPUTED
        and observation.status
        is not RuleObservationStatus.DISPUTED
    ):
        raise ValueError(
            "disputed evaluation only permits "
            "DISPUTED observation"
        )

    return RuleObservationBinding(
        observation_id=observation.observation_id,
        rule_id=evaluation.rule_id,
        rule_type=evaluation.rule_type,
        snapshot_id=evaluation.snapshot_id,
        snapshot_version=evaluation.snapshot_version,
        case_id=evaluation.case_id,
        evaluation_status=evaluation.status,
        observation_status=observation.status,
        dimension_results=(
            evaluation.dimension_results
        ),
        evidence_ids=(
            observation.evidence_ids
        ),
    )
