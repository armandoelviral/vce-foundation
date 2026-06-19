from phase3.admission_control_engine.admission_policy_record import (
    AdmissionPolicyRecord,
)

from phase3.trust_policy_engine.trust_decision import (
    TrustDecision,
)


class AdmissionEvaluation:

    @staticmethod
    def evaluate(
        policy: AdmissionPolicyRecord,
        trust_decision: TrustDecision,
    ) -> bool:

        return (
            trust_decision.status
            == "TRUSTED"
        )
