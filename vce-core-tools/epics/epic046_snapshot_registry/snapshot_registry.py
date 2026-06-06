class SnapshotRegistry:

    def __init__(self):
        self._snapshots = {}

    def add(self, snapshot):
        self._snapshots[
            snapshot.sequence
        ] = snapshot

    def get(self, sequence):
        return self._snapshots.get(
            sequence
        )

    def latest(self):

        if not self._snapshots:
            return None

        latest_sequence = max(
            self._snapshots.keys()
        )

        return self._snapshots[
            latest_sequence
        ]
