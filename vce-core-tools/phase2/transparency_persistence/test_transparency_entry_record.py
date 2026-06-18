from phase2.transparency_persistence.transparency_entry_record import (
    TransparencyEntryRecord,
)


def test_entry_contains_id():

    entry = TransparencyEntryRecord(
        entry_id="entry-001",
        entry_hash="hash-001",
    )

    assert entry.entry_id == "entry-001"


def test_entry_contains_hash():

    entry = TransparencyEntryRecord(
        entry_id="entry-001",
        entry_hash="hash-001",
    )

    assert entry.entry_hash == "hash-001"


def test_entry_serializes():

    entry = TransparencyEntryRecord(
        entry_id="entry-001",
        entry_hash="hash-001",
    )

    assert entry.to_dict() == {
        "entry_id": "entry-001",
        "entry_hash": "hash-001",
    }
