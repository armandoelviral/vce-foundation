from epics.epic043_snapshot_object.snapshot import Snapshot
from epics.epic048_seal_snapshot_opcode.seal_snapshot import (
    SealSnapshotOpcode,
)


def test_seals_snapshot():

    snapshot = Snapshot(
        sequence=10,
        state_hash="abc",
    )

    opcode = SealSnapshotOpcode()

    attestation = opcode.execute(
        snapshot
    )

    assert attestation.sequence == 10
    assert attestation.state_hash == "abc"
