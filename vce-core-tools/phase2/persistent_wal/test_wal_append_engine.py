from pathlib import Path

from phase2.persistent_wal.wal_append_engine import (
    WALAppendEngine,
)


def test_append_creates_wal_file(tmp_path):

    wal_path = tmp_path / "runtime.wal"

    engine = WALAppendEngine(
        wal_path=wal_path,
    )

    engine.append(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={
            "id": "event-001",
        },
    )

    assert wal_path.exists()


def test_append_writes_one_record(tmp_path):

    wal_path = tmp_path / "runtime.wal"

    engine = WALAppendEngine(
        wal_path=wal_path,
    )

    engine.append(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={
            "id": "event-001",
        },
    )

    lines = wal_path.read_text().splitlines()

    assert len(lines) == 1


def test_first_record_uses_genesis_hash(tmp_path):

    wal_path = tmp_path / "runtime.wal"

    engine = WALAppendEngine(
        wal_path=wal_path,
    )

    record = engine.append(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={},
    )

    assert record.previous_hash == "GENESIS"
