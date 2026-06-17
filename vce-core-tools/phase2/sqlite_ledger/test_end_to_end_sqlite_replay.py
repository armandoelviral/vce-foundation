from phase2.sqlite_ledger.sqlite_schema import (
    SQLiteLedgerSchema,
)

from phase2.sqlite_ledger.sqlite_append_engine import (
    SQLiteAppendEngine,
)

from phase2.sqlite_ledger.sqlite_integrity_verifier import (
    SQLiteIntegrityVerifier,
)

from phase2.sqlite_ledger.replay_query_loader import (
    ReplayQueryLoader,
)

from phase2.sqlite_ledger.snapshot_persistence import (
    SnapshotPersistence,
)


def test_end_to_end_sqlite_replay_flow(
    tmp_path,
):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    appender = SQLiteAppendEngine(
        db_path
    )

    appender.append(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={
            "id": "event-001",
        },
    )

    appender.append(
        lsn=2,
        opcode="REGISTER_ARTIFACT",
        payload={
            "artifact_id": "artifact-001",
        },
    )

    verifier = SQLiteIntegrityVerifier(
        db_path
    )

    assert verifier.verify()

    loader = ReplayQueryLoader(
        db_path
    )

    events = loader.load()

    assert len(events) == 2

    assert (
        events[0]["opcode"]
        == "APPEND_EVENT"
    )

    assert (
        events[1]["opcode"]
        == "REGISTER_ARTIFACT"
    )

    snapshots = SnapshotPersistence(
        db_path
    )

    snapshots.initialize()

    snapshots.save(
        snapshot_id="snapshot-001",
        lsn=2,
        state_hash="state-hash-001",
    )

    latest = snapshots.latest()

    assert (
        latest["snapshot_id"]
        == "snapshot-001"
    )

    assert (
        latest["lsn"]
        == 2
    )

    assert (
        latest["state_hash"]
        == "state-hash-001"
    )
