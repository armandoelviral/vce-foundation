from phase3.historical_governance_replay.historical_governance_snapshot import (
    HistoricalGovernanceSnapshot,
)


class GovernanceSnapshotRegistry:

    def __init__(self):

        self._snapshots = {}

    def add(
        self,
        snapshot: HistoricalGovernanceSnapshot,
    ) -> None:

        self._snapshots[
            snapshot.snapshot_id
        ] = snapshot

    def get(
        self,
        snapshot_id: str,
    ):

        return self._snapshots.get(
            snapshot_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._snapshots
        )

    def snapshot_ids(
        self,
    ):

        return list(
            self._snapshots.keys()
        )
