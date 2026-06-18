from phase3.historical_replay_auditor.historical_replay_record import (
    HistoricalReplayRecord,
)

from phase3.historical_replay_auditor.historical_replay_store import (
    HistoricalReplayStore,
)


def test_store_starts_empty():

    store = HistoricalReplayStore()

    assert store.count() == 0


def test_store_accepts_record():

    store = HistoricalReplayStore()

    record = HistoricalReplayRecord(
        replay_id="replay-001",
        bundle_id="bundle-001",
    )

    store.add(record)

    assert store.count() == 1


def test_store_returns_record():

    store = HistoricalReplayStore()

    record = HistoricalReplayRecord(
        replay_id="replay-001",
        bundle_id="bundle-001",
    )

    store.add(record)

    recovered = store.get(
        "replay-001"
    )

    assert recovered == record


def test_missing_record_returns_none():

    store = HistoricalReplayStore()

    assert store.get(
        "missing"
    ) is None
