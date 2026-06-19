from phase3.runtime_enforcement_engine.enforcement_policy_record import (
    EnforcementPolicyRecord,
)


class EnforcementPolicyRegistry:

    def __init__(self):

        self._policies = {}

    def add(
        self,
        policy: EnforcementPolicyRecord,
    ) -> None:

        self._policies[
            policy.policy_id
        ] = policy

    def get(
        self,
        policy_id: str,
    ):

        return self._policies.get(
            policy_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._policies
        )
