from phase3.runtime_governance.governance_policy_record import (
    GovernancePolicyRecord,
)

from phase3.runtime_enforcement_engine.enforcement_decision import (
    EnforcementDecision,
)


class GovernanceEvaluation:

    @staticmethod
    def evaluate(
        policy: GovernancePolicyRecord,
        enforcement_decision: EnforcementDecision,
    ) -> bool:

        return (
            enforcement_decision.status
            == "EXECUTE"
        )
