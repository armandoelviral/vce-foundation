class HistoricalReplayReport:

    def __init__(
        self,
        snapshots,
    ):

        self.snapshots = snapshots

    def snapshot_count(
        self,
    ) -> int:

        return len(
            self.snapshots
        )

    def snapshot_ids(
        self,
    ):

        return list(
            self.snapshots.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "snapshot_count":
                self.snapshot_count(),

            "snapshot_ids":
                self.snapshot_ids(),
        }
