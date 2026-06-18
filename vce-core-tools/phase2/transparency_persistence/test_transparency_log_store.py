from phase2.transparency_persistence.transparency_entry_record import (
    TransparencyEntryRecord,
)

from phase2.transparency_persistence.transparency_log_store import (
    TransparencyLogStore,
)


def test_store_starts_empty():

    store = TransparencyLogStore()

    assert store.count() == 0


def test_store_accepts_entry():

    store = TransparencyLogStore()

    entry = TransparencyEntryRecord(
        entry_id="entry-001",
        entry_hash="hash-001",
    )

    store.add(entry)

    assert store.count() == 1


def test_store_returns_entry():

    store = TransparencyLogStore()

    entry = TransparencyEntryRecord(
        entry_id="entry-001",
        entry_hash="hash-001",
    )

    store.add(entry)

    recovered = store.get(
        "entry-001"
    )

    assert recovered == entry


def test_unknown_entry_returns_none():

    store = TransparencyLogStore()

    assert store.get(
        "missing"
    ) is None
