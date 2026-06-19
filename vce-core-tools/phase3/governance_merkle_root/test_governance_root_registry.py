from phase3.governance_merkle_root.governance_merkle_root_record import (
    GovernanceMerkleRootRecord,
)

from phase3.governance_merkle_root.governance_root_registry import (
    GovernanceRootRegistry,
)


def test_registry_starts_empty():

    registry = GovernanceRootRegistry()

    assert registry.count() == 0


def test_registry_accepts_root():

    registry = GovernanceRootRegistry()

    root = GovernanceMerkleRootRecord(
        root_id="root-001",
        root_hash="root-hash-001",
        leaf_count=3,
    )

    registry.add(root)

    assert registry.count() == 1


def test_registry_returns_root():

    registry = GovernanceRootRegistry()

    root = GovernanceMerkleRootRecord(
        root_id="root-001",
        root_hash="root-hash-001",
        leaf_count=3,
    )

    registry.add(root)

    recovered = registry.get(
        "root-001"
    )

    assert recovered == root


def test_missing_root_returns_none():

    registry = GovernanceRootRegistry()

    assert registry.get(
        "missing"
    ) is None


def test_registry_lists_root_ids():

    registry = GovernanceRootRegistry()

    registry.add(
        GovernanceMerkleRootRecord(
            root_id="root-001",
            root_hash="root-hash-001",
            leaf_count=3,
        )
    )

    registry.add(
        GovernanceMerkleRootRecord(
            root_id="root-002",
            root_hash="root-hash-002",
            leaf_count=5,
        )
    )

    assert registry.root_ids() == [
        "root-001",
        "root-002",
    ]
