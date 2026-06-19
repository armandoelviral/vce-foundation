from phase3.governance_merkle_root.governance_root_registry import (
    GovernanceRootRegistry,
)


class RootQuery:

    def __init__(
        self,
        registry: GovernanceRootRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        root_id: str,
    ):

        return self.registry.get(
            root_id
        )
