from epics.epic047_snapshot_attestation.snapshot_attestor import (
    SnapshotAttestor,
)


class SealSnapshotOpcode:

    def __init__(self):
        self.attestor = SnapshotAttestor()

    def execute(self, snapshot):

        return self.attestor.attest(
            snapshot
        )
