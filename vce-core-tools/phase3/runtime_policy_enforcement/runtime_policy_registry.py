from phase3.runtime_policy_enforcement.runtime_policy_record import (
    RuntimePolicyRecord,
)


class RuntimePolicyRegistry:

    def __init__(self):

        self._policies = {}

    def add(
        self,
        policy: RuntimePolicyRecord,
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

    def policy_ids(
        self,
    ):

        return list(
            self._policies.keys()
        )
