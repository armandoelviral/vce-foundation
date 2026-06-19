from phase3.governance_merkle_history.governance_merkle_registry import (
    GovernanceMerkleRegistry,
)


class MerkleHistoryQuery:

    def __init__(
        self,
        registry: GovernanceMerkleRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        leaf_id: str,
    ):

        return self.registry.get(
            leaf_id
        )
