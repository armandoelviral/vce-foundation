from phase3.runtime_policy_enforcement.runtime_policy_record import (
    RuntimePolicyRecord,
)

from phase3.governance_execution_engine.execution_request_record import (
    ExecutionRequestRecord,
)


class ExecutionAuthorization:

    @staticmethod
    def authorize(
        request: ExecutionRequestRecord,
        policy: RuntimePolicyRecord,
    ) -> bool:

        if (
            request.resource_type
            != policy.resource_type
        ):
            return False

        if (
            request.action
            != policy.action
        ):
            return False

        return (
            policy.effect
            == "ALLOW"
        )
