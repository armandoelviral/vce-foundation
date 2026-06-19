from phase3.governance_consensus_resolution.consensus_registry import (
    ConsensusRegistry,
)


class ConsensusQuery:

    def __init__(
        self,
        registry: ConsensusRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        consensus_id: str,
    ):

        return self.registry.get(
            consensus_id
        )
