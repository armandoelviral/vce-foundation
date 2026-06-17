from phase2.persistent_wal.wal_append_engine import (
    WALAppendEngine,
)

from phase2.persistent_wal.wal_read_engine import (
    WALReadEngine,
)

from phase2.persistent_wal.wal_integrity_verifier import (
    WALIntegrityVerifier,
)

from phase2.persistent_wal.wal_replay_loader import (
    WALReplayLoader,
)

from phase2.persistent_wal.wal_snapshot import (
    WALSnapshot,
)


def test_end_to_end_persistent_replay_flow(tmp_path):

    wal_path = tmp_path / "runtime.wal"

    writer = WALAppendEngine(
        wal_path=wal_path,
    )

    writer.append(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={
            "id": "event-001",
        },
    )

    writer.append(
        lsn=2,
        opcode="REGISTER_ARTIFACT",
        payload={
            "artifact_id": "artifact-001",
        },
    )

    reader = WALReadEngine(
        wal_path=wal_path,
    )

    records = reader.read_all()

    assert len(records) == 2

    verifier = WALIntegrityVerifier(
        wal_path=wal_path,
    )

    assert verifier.verify()

    loader = WALReplayLoader(
        wal_path=wal_path,
    )

    events = loader.load()

    assert events[0]["opcode"] == "APPEND_EVENT"
    assert events[1]["opcode"] == "REGISTER_ARTIFACT"

    snapshot = WALSnapshot(
        lsn=2,
        state_hash=records[-1].current_hash,
    )

    assert snapshot.lsn == 2
    assert snapshot.state_hash == records[-1].current_hash
