from phase3.runtime_enforcement_engine.enforcement_policy_record import (
    EnforcementPolicyRecord,
)

from phase3.admission_control_engine.admission_decision import (
    AdmissionDecision,
)


class EnforcementEvaluation:

    @staticmethod
    def evaluate(
        policy: EnforcementPolicyRecord,
        admission_decision: AdmissionDecision,
    ) -> str:

        if (
            admission_decision.status
            == "ALLOW"
        ):
            return "EXECUTE"

        return "BLOCK"
