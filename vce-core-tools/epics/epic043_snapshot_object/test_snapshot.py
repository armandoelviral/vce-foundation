from epics.epic043_snapshot_object.snapshot import Snapshot


def test_snapshot_stores_sequence_and_state_hash():

    snapshot = Snapshot(
        sequence=3,
        state_hash="abc123",
    )

    assert snapshot.sequence == 3
    assert snapshot.state_hash == "abc123"
