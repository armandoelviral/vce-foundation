from phase3.trust_policy_engine.trust_policy_record import (
    TrustPolicyRecord,
)


class TrustPolicyRegistry:

    def __init__(self):

        self._policies = {}

    def add(
        self,
        policy: TrustPolicyRecord,
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
