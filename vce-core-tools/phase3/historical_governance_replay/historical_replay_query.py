from phase3.historical_governance_replay.governance_snapshot_registry import (
    GovernanceSnapshotRegistry,
)


class HistoricalReplayQuery:

    def __init__(
        self,
        registry: GovernanceSnapshotRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        snapshot_id: str,
    ):

        return self.registry.get(
            snapshot_id
        )
