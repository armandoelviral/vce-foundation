from epics.epic044_snapshot_builder.snapshot_builder import SnapshotBuilder


class SnapshotValidator:

    def __init__(self):
        self.builder = SnapshotBuilder()

    def validate(self, events, snapshot):
        rebuilt = self.builder.build(events)

        return rebuilt == snapshot
