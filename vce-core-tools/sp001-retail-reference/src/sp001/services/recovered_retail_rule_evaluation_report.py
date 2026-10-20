from dataclasses import dataclass

from sp001.contracts.retail_rule_evaluation_admission import (
    RetailRuleEvaluationAdmission,
)
from sp001.services.retail_rule_evaluation_report import RetailRuleEvaluationReport


@dataclass(frozen=True, slots=True)
class RecoveredRetailRuleEvaluationReport:
    """Report and matching locally recorded admissions at one read snapshot.

    Does not establish external integrity or the report's original admission path.
    Missing admissions remain explicitly declared attribution.
    """

    report: RetailRuleEvaluationReport
    admissions: tuple[RetailRuleEvaluationAdmission, ...]

    def __post_init__(self):
        if type(self.report) is not RetailRuleEvaluationReport:
            raise TypeError("report must be a RetailRuleEvaluationReport")
        if type(self.admissions) is not tuple:
            raise TypeError("admissions must be a tuple")
        if any(type(item) is not RetailRuleEvaluationAdmission
               for item in self.admissions):
            raise TypeError("invalid admission")
        evaluations = {
            item.evaluation_id: item for item in self.report.evaluations
        }
        ids = tuple(item.evaluation.evaluation_id for item in self.admissions)
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate admission")
        for item in self.admissions:
            if evaluations.get(item.evaluation.evaluation_id) != item.evaluation:
                raise ValueError("admission differs from report evaluation")
        expected_order = tuple(
            item.evaluation_id for item in self.report.evaluations
            if item.evaluation_id in set(ids)
        )
        if ids != expected_order:
            raise ValueError("admissions must follow report evaluation order")

    @property
    def declared_only_evaluation_ids(self) -> tuple[str, ...]:
        recorded = {
            item.evaluation.evaluation_id for item in self.admissions
        }
        return tuple(
            item.evaluation_id for item in self.report.evaluations
            if item.evaluation_id not in recorded
        )
