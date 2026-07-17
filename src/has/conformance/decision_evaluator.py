from __future__ import annotations

from has.conformance.model.conformance_input import (
    ConformanceInput,
)
from has.conformance.model.decision import Decision
from has.conformance.model.decision_record import (
    DecisionRecord,
)
from has.conformance.model.evidence import Evidence
from has.conformance.policies.covered_policy import (
    CoveredPolicy,
)
from has.conformance.policies.decision_policy import (
    DecisionPolicy,
)


class ConformanceDecisionEvaluator:
    """
    Deterministic evaluator that delegates
    normative decision rules to a policy.
    """

    def __init__(
        self,
        policy: DecisionPolicy | None = None,
    ) -> None:
        self._policy = (
            policy
            if policy is not None
            else CoveredPolicy()
        )

    def evaluate(
        self,
        conformance_input: ConformanceInput,
        evidence: Evidence,
    ) -> DecisionRecord:
        decision = self._policy.evaluate(
            conformance_input,
            evidence,
        )

        failure_reason = (
            None
            if decision is Decision.CONFORMANT
            else "non_conformant"
        )

        return DecisionRecord(
            claim=conformance_input.claim,
            capability=conformance_input.capability,
            executable_contract=(
                conformance_input.executable_contract
            ),
            coverage_status=(
                conformance_input.coverage_status
            ),
            decision=decision,
            evidence=evidence,
            failure_reason=failure_reason,
        )
