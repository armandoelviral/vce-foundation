from phase3.runtime_policy_enforcement.runtime_policy_record import (
    RuntimePolicyRecord,
)


class RuntimePolicyEvaluation:

    @staticmethod
    def evaluate(
        policy: RuntimePolicyRecord,
        resource_type: str,
        action: str,
    ) -> bool:

        if (
            policy.resource_type
            != resource_type
        ):
            return False

        if (
            policy.action
            != action
        ):
            return False

        return (
            policy.effect
            == "ALLOW"
        )
