from phase2.persistent_wal.wal_append_engine import (
    WALAppendEngine,
)

from phase2.persistent_wal.wal_replay_loader import (
    WALReplayLoader,
)


def test_load_empty_wal_returns_empty_list(tmp_path):

    loader = WALReplayLoader(
        wal_path=tmp_path / "runtime.wal",
    )

    assert loader.load() == []


def test_load_returns_events_in_order(tmp_path):

    wal_path = tmp_path / "runtime.wal"

    writer = WALAppendEngine(
        wal_path=wal_path,
    )

    writer.append(
        lsn=1,
        opcode="EVENT_A",
        payload={"value": 1},
    )

    writer.append(
        lsn=2,
        opcode="EVENT_B",
        payload={"value": 2},
    )

    loader = WALReplayLoader(
        wal_path=wal_path,
    )

    events = loader.load()

    assert len(events) == 2

    assert events[0]["opcode"] == "EVENT_A"

    assert events[1]["opcode"] == "EVENT_B"


def test_load_preserves_payload(tmp_path):

    wal_path = tmp_path / "runtime.wal"

    writer = WALAppendEngine(
        wal_path=wal_path,
    )

    writer.append(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={
            "artifact_id": "artifact-001",
        },
    )

    loader = WALReplayLoader(
        wal_path=wal_path,
    )

    events = loader.load()

    assert (
        events[0]["payload"]["artifact_id"]
        == "artifact-001"
    )


def test_load_preserves_lsn_order(tmp_path):

    wal_path = tmp_path / "runtime.wal"

    writer = WALAppendEngine(
        wal_path=wal_path,
    )

    writer.append(
        lsn=10,
        opcode="EVENT_A",
        payload={},
    )

    writer.append(
        lsn=11,
        opcode="EVENT_B",
        payload={},
    )

    loader = WALReplayLoader(
        wal_path=wal_path,
    )

    events = loader.load()

    assert events[0]["lsn"] == 10

    assert events[1]["lsn"] == 11
