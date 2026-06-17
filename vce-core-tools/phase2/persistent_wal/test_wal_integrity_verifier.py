import json

from phase2.persistent_wal.wal_append_engine import (
    WALAppendEngine,
)

from phase2.persistent_wal.wal_integrity_verifier import (
    WALIntegrityVerifier,
)


def test_accepts_valid_wal(tmp_path):

    wal_path = tmp_path / "runtime.wal"

    writer = WALAppendEngine(
        wal_path=wal_path,
    )

    writer.append(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={"id": "event-001"},
    )

    writer.append(
        lsn=2,
        opcode="APPEND_EVENT",
        payload={"id": "event-002"},
    )

    verifier = WALIntegrityVerifier(
        wal_path=wal_path,
    )

    assert verifier.verify()


def test_detects_modified_payload(tmp_path):

    wal_path = tmp_path / "runtime.wal"

    writer = WALAppendEngine(
        wal_path=wal_path,
    )

    writer.append(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={"id": "event-001"},
    )

    lines = wal_path.read_text(
        encoding="utf-8"
    ).splitlines()

    record = json.loads(
        lines[0]
    )

    record["payload"]["id"] = "forged"

    wal_path.write_text(
        json.dumps(record) + "\n",
        encoding="utf-8",
    )

    verifier = WALIntegrityVerifier(
        wal_path=wal_path,
    )

    assert not verifier.verify()


def test_detects_broken_hash_chain(tmp_path):

    wal_path = tmp_path / "runtime.wal"

    writer = WALAppendEngine(
        wal_path=wal_path,
    )

    writer.append(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={"id": "event-001"},
    )

    writer.append(
        lsn=2,
        opcode="APPEND_EVENT",
        payload={"id": "event-002"},
    )

    lines = wal_path.read_text(
        encoding="utf-8"
    ).splitlines()

    second = json.loads(
        lines[1]
    )

    second["previous_hash"] = "FAKE_HASH"

    lines[1] = json.dumps(
        second
    )

    wal_path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    verifier = WALIntegrityVerifier(
        wal_path=wal_path,
    )

    assert not verifier.verify()
