from dataclasses import dataclass
from datetime import datetime

from sp001.contracts.retail_context_rule_observation import (
    RetailContextRuleObservation,
)
from sp001.contracts.retail_process_actor import RetailProcessActor
from sp001.contracts.retail_rule_criterion import RetailRuleCriterion


@dataclass(frozen=True, slots=True)
class RetailRuleEvaluationRecord:
    """Declared evaluation occurrence; does not authenticate or authorize."""

    evaluation_id: str
    observation: RetailContextRuleObservation
    criterion: RetailRuleCriterion
    evaluator: RetailProcessActor
    evaluated_at: datetime
    rationale: str

    def __post_init__(self) -> None:
        for name in ("evaluation_id", "rationale"):
            value = getattr(self, name)
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if not value.strip():
                raise ValueError(f"{name} must not be empty")

        for name, expected in (
            ("observation", RetailContextRuleObservation),
            ("criterion", RetailRuleCriterion),
            ("evaluator", RetailProcessActor),
        ):
            if not isinstance(getattr(self, name), expected):
                raise TypeError(f"{name} must be a {expected.__name__}")

        if self.observation.rule_id != self.criterion.rule_id:
            raise ValueError("observation and criterion rule_id must match")

        if not isinstance(self.evaluated_at, datetime):
            raise TypeError("evaluated_at must be a datetime")
        if (
            self.evaluated_at.tzinfo is None
            or self.evaluated_at.utcoffset() is None
        ):
            raise ValueError("evaluated_at must be timezone-aware")
