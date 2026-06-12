from dataclasses import dataclass


@dataclass(frozen=True)
class GovernancePolicy:
    policy_id: str
    policy_version: str
    policy_hash: str
    active: bool


class PolicyRegistry:

    def __init__(self):

        self._policies = {}

    def register(
        self,
        policy: GovernancePolicy,
    ):

        key = (
            policy.policy_id,
            policy.policy_version,
        )

        self._policies[
            key
        ] = policy

    def get(
        self,
        policy_id,
        policy_version,
    ):

        return self._policies.get(
            (
                policy_id,
                policy_version,
            )
        )

    def is_registered(
        self,
        policy_id,
        policy_version,
    ):

        policy = self.get(
            policy_id,
            policy_version,
        )

        return (
            policy is not None
            and policy.active is True
        )
