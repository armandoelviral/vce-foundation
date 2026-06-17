from phase2.sqlite_ledger.sqlite_schema import (
    SQLiteLedgerSchema,
)

from phase2.sqlite_ledger.sqlite_append_engine import (
    SQLiteAppendEngine,
)

from phase2.sqlite_ledger.replay_query_loader import (
    ReplayQueryLoader,
)


def test_load_returns_empty_list_for_empty_ledger(
    tmp_path,
):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    loader = ReplayQueryLoader(
        db_path
    )

    assert loader.load() == []


def test_load_returns_events_in_lsn_order(
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
        opcode="EVENT_A",
        payload={"value": 1},
    )

    appender.append(
        lsn=2,
        opcode="EVENT_B",
        payload={"value": 2},
    )

    loader = ReplayQueryLoader(
        db_path
    )

    events = loader.load()

    assert len(events) == 2

    assert (
        events[0]["opcode"]
        == "EVENT_A"
    )

    assert (
        events[1]["opcode"]
        == "EVENT_B"
    )


def test_load_preserves_payload(
    tmp_path,
):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    SQLiteAppendEngine(
        db_path
    ).append(
        lsn=1,
        opcode="REGISTER_ARTIFACT",
        payload={
            "artifact_id": "artifact-001",
        },
    )

    loader = ReplayQueryLoader(
        db_path
    )

    events = loader.load()

    assert (
        events[0]["payload"]["artifact_id"]
        == "artifact-001"
    )


def test_load_preserves_lsn(
    tmp_path,
):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    SQLiteAppendEngine(
        db_path
    ).append(
        lsn=42,
        opcode="EVENT_A",
        payload={},
    )

    loader = ReplayQueryLoader(
        db_path
    )

    events = loader.load()

    assert (
        events[0]["lsn"]
        == 42
    )
