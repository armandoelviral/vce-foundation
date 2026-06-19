from phase3.policy_versioning.policy_version_registry import (
    PolicyVersionRegistry,
)


class PolicyVersionQuery:

    def __init__(
        self,
        registry: PolicyVersionRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        version_id: str,
    ):

        return self.registry.get(
            version_id
        )
