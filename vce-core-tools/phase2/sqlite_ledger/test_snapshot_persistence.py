from phase2.sqlite_ledger.sqlite_schema import (
    SQLiteLedgerSchema,
)

from phase2.sqlite_ledger.snapshot_persistence import (
    SnapshotPersistence,
)


def test_snapshot_table_exists_after_initialize(tmp_path):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    snapshots = SnapshotPersistence(
        db_path
    )

    snapshots.initialize()

    assert snapshots.count() == 0


def test_persist_snapshot(tmp_path):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    snapshots = SnapshotPersistence(
        db_path
    )

    snapshots.initialize()

    snapshots.save(
        snapshot_id="snapshot-001",
        lsn=10,
        state_hash="state-001",
    )

    assert snapshots.count() == 1


def test_load_latest_snapshot(tmp_path):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    snapshots = SnapshotPersistence(
        db_path
    )

    snapshots.initialize()

    snapshots.save(
        snapshot_id="snapshot-001",
        lsn=10,
        state_hash="state-001",
    )

    snapshots.save(
        snapshot_id="snapshot-002",
        lsn=20,
        state_hash="state-002",
    )

    latest = snapshots.latest()

    assert latest["snapshot_id"] == "snapshot-002"
    assert latest["lsn"] == 20
    assert latest["state_hash"] == "state-002"


def test_latest_returns_none_when_empty(tmp_path):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    snapshots = SnapshotPersistence(
        db_path
    )

    snapshots.initialize()

    assert snapshots.latest() is None
