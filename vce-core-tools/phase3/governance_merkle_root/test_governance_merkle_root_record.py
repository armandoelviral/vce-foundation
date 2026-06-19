from phase3.governance_merkle_root.governance_merkle_root_record import (
    GovernanceMerkleRootRecord,
)


def test_contains_root_id():

    record = GovernanceMerkleRootRecord(
        root_id="root-001",
        root_hash="root-hash-001",
        leaf_count=3,
    )

    assert record.root_id == "root-001"


def test_contains_root_hash():

    record = GovernanceMerkleRootRecord(
        root_id="root-001",
        root_hash="root-hash-001",
        leaf_count=3,
    )

    assert (
        record.root_hash
        == "root-hash-001"
    )


def test_contains_leaf_count():

    record = GovernanceMerkleRootRecord(
        root_id="root-001",
        root_hash="root-hash-001",
        leaf_count=3,
    )

    assert record.leaf_count == 3


def test_serializes():

    record = GovernanceMerkleRootRecord(
        root_id="root-001",
        root_hash="root-hash-001",
        leaf_count=3,
    )

    assert record.to_dict() == {
        "root_id": "root-001",
        "root_hash": "root-hash-001",
        "leaf_count": 3,
    }
