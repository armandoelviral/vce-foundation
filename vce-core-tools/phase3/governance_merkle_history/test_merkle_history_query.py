from phase3.governance_merkle_history.governance_merkle_leaf import (
    GovernanceMerkleLeaf,
)

from phase3.governance_merkle_history.governance_merkle_registry import (
    GovernanceMerkleRegistry,
)

from phase3.governance_merkle_history.merkle_history_query import (
    MerkleHistoryQuery,
)


def test_query_returns_leaf():

    registry = GovernanceMerkleRegistry()

    leaf = GovernanceMerkleLeaf(
        leaf_id="leaf-001",
        snapshot_id="snap-001",
        hash_value="hash-001",
    )

    registry.add(leaf)

    query = MerkleHistoryQuery(registry)

    result = query.by_id(
        "leaf-001"
    )

    assert result == leaf


def test_query_returns_none_for_missing():

    registry = GovernanceMerkleRegistry()

    query = MerkleHistoryQuery(registry)

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_snapshot_id():

    registry = GovernanceMerkleRegistry()

    leaf = GovernanceMerkleLeaf(
        leaf_id="leaf-001",
        snapshot_id="snap-001",
        hash_value="hash-001",
    )

    registry.add(leaf)

    query = MerkleHistoryQuery(registry)

    result = query.by_id(
        "leaf-001"
    )

    assert (
        result.snapshot_id
        == "snap-001"
    )
