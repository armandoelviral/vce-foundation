from dataclasses import dataclass

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_evaluator_binding import (
    RetailEvaluatorBindingSnapshot,
)
from sp001.contracts.retail_rule_evaluation_record import (
    RetailRuleEvaluationRecord,
)


@dataclass(frozen=True, slots=True)
class RetailRuleEvaluationAdmission:
    """Declared attribution admission record, not proof of durable acceptance.

    Construction establishes neither authentication nor current binding state.
    validated_at records the asserted validation instant, not the commit time.
    Historical recovery preserves this record without requiring current validity.
    """

    evaluation: RetailRuleEvaluationRecord
    principal: AuthenticatedPrincipal
    binding_snapshot: RetailEvaluatorBindingSnapshot
    validated_at: int

    def __post_init__(self) -> None:
        for name, expected in (
            ("evaluation", RetailRuleEvaluationRecord),
            ("principal", AuthenticatedPrincipal),
            ("binding_snapshot", RetailEvaluatorBindingSnapshot),
        ):
            if not isinstance(getattr(self, name), expected):
                raise TypeError(f"{name} must be a {expected.__name__}")

        if type(self.validated_at) is not int:
            raise TypeError("validated_at must be integer Unix seconds")
        if self.validated_at < 0:
            raise ValueError("validated_at must be nonnegative")

        binding = self.binding_snapshot.binding
        if binding.principal != self.principal:
            raise ValueError("admission principal differs from binding")
        if binding.actor != self.evaluation.evaluator:
            raise ValueError("admission evaluator differs from binding")
        if binding.case_id != self.evaluation.observation.case_id:
            raise ValueError("admission case differs from binding")
        if self.binding_snapshot.revoked:
            raise ValueError("admission binding snapshot is revoked")
        if not binding.valid_from <= self.validated_at < binding.expires_at:
            raise ValueError("validation instant is outside binding validity")
