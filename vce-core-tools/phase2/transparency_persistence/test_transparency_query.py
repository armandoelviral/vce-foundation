from phase2.transparency_persistence.transparency_entry_record import (
    TransparencyEntryRecord,
)

from phase2.transparency_persistence.transparency_log_store import (
    TransparencyLogStore,
)

from phase2.transparency_persistence.transparency_query import (
    TransparencyQuery,
)


def test_query_returns_entry_by_hash():

    store = TransparencyLogStore()

    store.add(
        TransparencyEntryRecord(
            entry_id="entry-001",
            entry_hash="hash-001",
        )
    )

    query = TransparencyQuery(store)

    results = query.by_hash(
        "hash-001"
    )

    assert len(results) == 1
    assert results[0].entry_id == "entry-001"


def test_query_returns_empty_for_unknown_hash():

    store = TransparencyLogStore()

    query = TransparencyQuery(store)

    assert query.by_hash(
        "missing"
    ) == []


def test_query_filters_multiple_hashes():

    store = TransparencyLogStore()

    store.add(
        TransparencyEntryRecord(
            entry_id="entry-001",
            entry_hash="hash-001",
        )
    )

    store.add(
        TransparencyEntryRecord(
            entry_id="entry-002",
            entry_hash="hash-002",
        )
    )

    query = TransparencyQuery(store)

    results = query.by_hash(
        "hash-002"
    )

    assert len(results) == 1
    assert results[0].entry_id == "entry-002"
