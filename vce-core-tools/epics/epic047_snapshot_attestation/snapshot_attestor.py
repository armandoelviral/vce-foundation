from epics.epic047_snapshot_attestation.snapshot_attestation import (
    SnapshotAttestation,
)


class SnapshotAttestor:

    def attest(self, snapshot):

        return SnapshotAttestation(
            sequence=snapshot.sequence,
            state_hash=snapshot.state_hash,
        )
