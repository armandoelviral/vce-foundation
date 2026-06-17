from phase2.persistent_wal.wal_snapshot import (
    WALSnapshot,
)


def test_snapshot_contains_lsn():

    snapshot = WALSnapshot(
        lsn=10,
        state_hash="state-001",
    )

    assert snapshot.lsn == 10


def test_snapshot_contains_state_hash():

    snapshot = WALSnapshot(
        lsn=10,
        state_hash="state-001",
    )

    assert snapshot.state_hash == "state-001"


def test_snapshot_serializes():

    snapshot = WALSnapshot(
        lsn=10,
        state_hash="state-001",
    )

    assert snapshot.to_dict() == {
        "lsn": 10,
        "state_hash": "state-001",
    }
