from epics.epic043_snapshot_object.snapshot import Snapshot
from epics.epic047_snapshot_attestation.snapshot_attestation import (
    SnapshotAttestation,
)
from epics.epic047_snapshot_attestation.snapshot_attestor import (
    SnapshotAttestor,
)


def test_attestation_captures_snapshot():

    snapshot = Snapshot(
        sequence=42,
        state_hash="abc123",
    )

    attestation = SnapshotAttestor().attest(snapshot)

    assert isinstance(attestation, SnapshotAttestation)
    assert attestation.sequence == 42
    assert attestation.state_hash == "abc123"
