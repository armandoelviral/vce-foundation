from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.retail_rule_evaluation_record import (
    RetailRuleEvaluationRecord,
)


class RetailRuleEvaluationRelationType(StrEnum):
    JUDGMENT_REVIEW = "JUDGMENT_REVIEW"
    AFTER_DECLARED_INTERVENTION = "AFTER_DECLARED_INTERVENTION"


@dataclass(frozen=True, slots=True)
class RetailRuleEvaluationRelation:
    """Declared relationship; does not establish causality or supersession."""

    relation_id: str
    previous: RetailRuleEvaluationRecord
    current: RetailRuleEvaluationRecord
    relation_type: RetailRuleEvaluationRelationType
    rationale: str
    intervention_evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("relation_id", "rationale"):
            value = getattr(self, name)
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if not value.strip():
                raise ValueError(f"{name} must not be empty")

        for name in ("previous", "current"):
            if not isinstance(
                getattr(self, name), RetailRuleEvaluationRecord
            ):
                raise TypeError(
                    f"{name} must be a RetailRuleEvaluationRecord"
                )

        if not isinstance(
            self.relation_type, RetailRuleEvaluationRelationType
        ):
            raise TypeError(
                "relation_type must be a RetailRuleEvaluationRelationType"
            )

        if self.previous.evaluation_id == self.current.evaluation_id:
            raise ValueError("evaluation identities must differ")
        if (
            self.previous.observation.case_id
            != self.current.observation.case_id
        ):
            raise ValueError("evaluations must belong to the same case")
        if self.previous.criterion.rule_id != self.current.criterion.rule_id:
            raise ValueError("evaluations must refer to the same rule")
        if self.current.evaluated_at < self.previous.evaluated_at:
            raise ValueError("current evaluation must not precede previous")

        # Reject contradictory content for the same declared criterion version.
        if (
            self.previous.criterion.criterion_version
            == self.current.criterion.criterion_version
            and self.previous.criterion != self.current.criterion
        ):
            raise ValueError("same criterion version has conflicting content")

        # An observation identity cannot silently acquire different content.
        if (
            self.previous.observation.observation_id
            == self.current.observation.observation_id
            and self.previous.observation != self.current.observation
        ):
            raise ValueError("same observation identity has conflicting content")

        if not isinstance(self.intervention_evidence_ids, tuple):
            raise TypeError("intervention_evidence_ids must be a tuple")
        seen = set()
        for identity in self.intervention_evidence_ids:
            if not isinstance(identity, str):
                raise TypeError("intervention evidence identity must be a string")
            if not identity.strip():
                raise ValueError("intervention evidence identity must not be empty")
            if identity in seen:
                raise ValueError("duplicate intervention evidence identity")
            seen.add(identity)

        if (
            self.relation_type
            is RetailRuleEvaluationRelationType.AFTER_DECLARED_INTERVENTION
            and not self.intervention_evidence_ids
        ):
            raise ValueError("declared intervention requires evidence references")
        if (
            self.relation_type
            is RetailRuleEvaluationRelationType.JUDGMENT_REVIEW
            and self.intervention_evidence_ids
        ):
            raise ValueError("judgment review must not declare intervention evidence")
