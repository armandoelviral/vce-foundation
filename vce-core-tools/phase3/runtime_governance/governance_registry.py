from phase3.runtime_governance.governance_policy_record import (
    GovernancePolicyRecord,
)


class GovernanceRegistry:

    def __init__(self):

        self._policies = {}

    def add(
        self,
        policy: GovernancePolicyRecord,
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
