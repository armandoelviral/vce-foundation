from epics.phase8_004_constitutional_snapshots.snapshot_record import (
    SnapshotRecord,
)


class SnapshotRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: SnapshotRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
