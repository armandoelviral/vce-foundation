from phase2.transparency_persistence.merkle_root_record import (
    MerkleRootRecord,
)


def test_root_contains_root_hash():

    root = MerkleRootRecord(
        root_hash="root-001",
        entry_count=5,
    )

    assert root.root_hash == "root-001"


def test_root_contains_entry_count():

    root = MerkleRootRecord(
        root_hash="root-001",
        entry_count=5,
    )

    assert root.entry_count == 5


def test_root_serializes():

    root = MerkleRootRecord(
        root_hash="root-001",
        entry_count=5,
    )

    assert root.to_dict() == {
        "root_hash": "root-001",
        "entry_count": 5,
    }
