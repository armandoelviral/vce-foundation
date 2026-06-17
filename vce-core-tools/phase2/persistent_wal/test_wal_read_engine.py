from phase2.persistent_wal.wal_append_engine import (
    WALAppendEngine,
)

from phase2.persistent_wal.wal_read_engine import (
    WALReadEngine,
)


def test_read_returns_empty_for_missing_wal(tmp_path):

    reader = WALReadEngine(
        wal_path=tmp_path / "missing.wal",
    )

    assert reader.read_all() == []


def test_read_returns_single_record(tmp_path):

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

    reader = WALReadEngine(
        wal_path=wal_path,
    )

    records = reader.read_all()

    assert len(records) == 1


def test_read_preserves_lsn(tmp_path):

    wal_path = tmp_path / "runtime.wal"

    writer = WALAppendEngine(
        wal_path=wal_path,
    )

    writer.append(
        lsn=42,
        opcode="APPEND_EVENT",
        payload={},
    )

    reader = WALReadEngine(
        wal_path=wal_path,
    )

    records = reader.read_all()

    assert records[0].lsn == 42


def test_read_preserves_hash_chain(tmp_path):

    wal_path = tmp_path / "runtime.wal"

    writer = WALAppendEngine(
        wal_path=wal_path,
    )

    writer.append(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={},
    )

    reader = WALReadEngine(
        wal_path=wal_path,
    )

    records = reader.read_all()

    assert (
        records[0].previous_hash
        == "GENESIS"
    )
