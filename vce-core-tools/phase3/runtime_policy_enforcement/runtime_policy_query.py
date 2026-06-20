from phase3.runtime_policy_enforcement.runtime_policy_registry import (
    RuntimePolicyRegistry,
)


class RuntimePolicyQuery:

    def __init__(
        self,
        registry: RuntimePolicyRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        policy_id: str,
    ):

        return self.registry.get(
            policy_id
        )
