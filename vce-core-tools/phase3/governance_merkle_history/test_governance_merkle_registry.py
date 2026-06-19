from phase3.governance_merkle_history.governance_merkle_leaf import (
    GovernanceMerkleLeaf,
)

from phase3.governance_merkle_history.governance_merkle_registry import (
    GovernanceMerkleRegistry,
)


def test_registry_starts_empty():

    registry = GovernanceMerkleRegistry()

    assert registry.count() == 0


def test_registry_accepts_leaf():

    registry = GovernanceMerkleRegistry()

    leaf = GovernanceMerkleLeaf(
        leaf_id="leaf-001",
        snapshot_id="snap-001",
        hash_value="hash-001",
    )

    registry.add(leaf)

    assert registry.count() == 1


def test_registry_returns_leaf():

    registry = GovernanceMerkleRegistry()

    leaf = GovernanceMerkleLeaf(
        leaf_id="leaf-001",
        snapshot_id="snap-001",
        hash_value="hash-001",
    )

    registry.add(leaf)

    recovered = registry.get(
        "leaf-001"
    )

    assert recovered == leaf


def test_missing_leaf_returns_none():

    registry = GovernanceMerkleRegistry()

    assert registry.get(
        "missing"
    ) is None


def test_registry_lists_leaf_ids():

    registry = GovernanceMerkleRegistry()

    registry.add(
        GovernanceMerkleLeaf(
            leaf_id="leaf-001",
            snapshot_id="snap-001",
            hash_value="hash-001",
        )
    )

    registry.add(
        GovernanceMerkleLeaf(
            leaf_id="leaf-002",
            snapshot_id="snap-002",
            hash_value="hash-002",
        )
    )

    assert registry.leaf_ids() == [
        "leaf-001",
        "leaf-002",
    ]
