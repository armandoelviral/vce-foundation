from phase3.governance_merkle_history.governance_merkle_leaf import (
    GovernanceMerkleLeaf,
)


def test_contains_leaf_id():

    leaf = GovernanceMerkleLeaf(
        leaf_id="leaf-001",
        snapshot_id="snap-001",
        hash_value="hash-001",
    )

    assert leaf.leaf_id == "leaf-001"


def test_contains_snapshot_id():

    leaf = GovernanceMerkleLeaf(
        leaf_id="leaf-001",
        snapshot_id="snap-001",
        hash_value="hash-001",
    )

    assert leaf.snapshot_id == "snap-001"


def test_contains_hash():

    leaf = GovernanceMerkleLeaf(
        leaf_id="leaf-001",
        snapshot_id="snap-001",
        hash_value="hash-001",
    )

    assert leaf.hash_value == "hash-001"


def test_serializes():

    leaf = GovernanceMerkleLeaf(
        leaf_id="leaf-001",
        snapshot_id="snap-001",
        hash_value="hash-001",
    )

    assert leaf.to_dict() == {
        "leaf_id": "leaf-001",
        "snapshot_id": "snap-001",
        "hash_value": "hash-001",
    }
