from phase3.governance_policy_enforcement.policy_activation_registry import (
    PolicyActivationRegistry,
)


class PolicyActivationQuery:

    def __init__(
        self,
        registry: PolicyActivationRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        activation_id: str,
    ):

        return self.registry.get(
            activation_id
        )
