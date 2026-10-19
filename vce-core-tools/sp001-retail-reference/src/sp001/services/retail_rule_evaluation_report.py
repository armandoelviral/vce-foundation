from dataclasses import dataclass

from sp001.contracts.retail_rule_evaluation_record import (
    RetailRuleEvaluationRecord,
)
from sp001.contracts.retail_rule_evaluation_relation import (
    RetailRuleEvaluationRelation,
)


@dataclass(frozen=True, slots=True)
class RetailRuleEvaluationReport:
    """Detailed in-memory records; no publication or acceptance claims."""

    case_id: str
    evaluations: tuple[RetailRuleEvaluationRecord, ...]
    relations: tuple[RetailRuleEvaluationRelation, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.case_id, str):
            raise TypeError("case_id must be a string")
        if not self.case_id.strip():
            raise ValueError("case_id must not be empty")
        if not isinstance(self.evaluations, tuple):
            raise TypeError("evaluations must be a tuple")
        if not self.evaluations:
            raise ValueError("evaluations must not be empty")
        if not isinstance(self.relations, tuple):
            raise TypeError("relations must be a tuple")

        by_id = {}
        criteria = {}
        observations = {}
        for record in self.evaluations:
            if not isinstance(record, RetailRuleEvaluationRecord):
                raise TypeError("invalid evaluation record")
            if record.observation.case_id != self.case_id:
                raise ValueError("evaluation case does not match report")
            if record.evaluation_id in by_id:
                raise ValueError("duplicate evaluation identity")
            by_id[record.evaluation_id] = record

            key = (
                record.criterion.rule_id,
                record.criterion.criterion_version,
            )
            if key in criteria and criteria[key] != record.criterion:
                raise ValueError("conflicting criterion version")
            criteria[key] = record.criterion

            key = record.observation.observation_id
            if key in observations and observations[key] != record.observation:
                raise ValueError("conflicting observation identity")
            observations[key] = record.observation

        relation_ids = set()
        for relation in self.relations:
            if not isinstance(relation, RetailRuleEvaluationRelation):
                raise TypeError("invalid evaluation relation")
            if relation.relation_id in relation_ids:
                raise ValueError("duplicate relation identity")
            relation_ids.add(relation.relation_id)
            for endpoint in (relation.previous, relation.current):
                stored = by_id.get(endpoint.evaluation_id)
                if stored is None:
                    raise ValueError("relation evaluation is absent")
                if stored != endpoint:
                    raise ValueError("relation evaluation content conflicts")


def build_retail_rule_evaluation_report(
    *,
    case_id: str,
    evaluations: tuple[RetailRuleEvaluationRecord, ...],
    relations: tuple[RetailRuleEvaluationRelation, ...] = (),
) -> RetailRuleEvaluationReport:
    """Preserve supplied records without choosing winners or inferring change."""
    return RetailRuleEvaluationReport(
        case_id=case_id,
        evaluations=evaluations,
        relations=relations,
    )
