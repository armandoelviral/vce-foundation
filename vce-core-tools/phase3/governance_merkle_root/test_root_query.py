from phase3.governance_merkle_root.governance_merkle_root_record import (
    GovernanceMerkleRootRecord,
)

from phase3.governance_merkle_root.governance_root_registry import (
    GovernanceRootRegistry,
)

from phase3.governance_merkle_root.root_query import (
    RootQuery,
)


def test_query_returns_root():

    registry = GovernanceRootRegistry()

    root = GovernanceMerkleRootRecord(
        root_id="root-001",
        root_hash="root-hash-001",
        leaf_count=3,
    )

    registry.add(root)

    query = RootQuery(
        registry
    )

    result = query.by_id(
        "root-001"
    )

    assert result == root


def test_query_returns_none_for_missing():

    registry = GovernanceRootRegistry()

    query = RootQuery(
        registry
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_root_hash():

    registry = GovernanceRootRegistry()

    root = GovernanceMerkleRootRecord(
        root_id="root-001",
        root_hash="root-hash-001",
        leaf_count=3,
    )

    registry.add(root)

    query = RootQuery(
        registry
    )

    result = query.by_id(
        "root-001"
    )

    assert (
        result.root_hash
        == "root-hash-001"
    )
