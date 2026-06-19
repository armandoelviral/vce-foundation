from phase3.historical_governance_replay.historical_governance_snapshot import (
    HistoricalGovernanceSnapshot,
)

from phase3.historical_governance_replay.governance_snapshot_registry import (
    GovernanceSnapshotRegistry,
)


def test_registry_starts_empty():

    registry = GovernanceSnapshotRegistry()

    assert registry.count() == 0


def test_registry_accepts_snapshot():

    registry = GovernanceSnapshotRegistry()

    snapshot = HistoricalGovernanceSnapshot(
        snapshot_id="snap-001",
        policy_version="trust-policy:v2",
        authority_id="auth-001",
    )

    registry.add(snapshot)

    assert registry.count() == 1


def test_registry_returns_snapshot():

    registry = GovernanceSnapshotRegistry()

    snapshot = HistoricalGovernanceSnapshot(
        snapshot_id="snap-001",
        policy_version="trust-policy:v2",
        authority_id="auth-001",
    )

    registry.add(snapshot)

    recovered = registry.get(
        "snap-001"
    )

    assert recovered == snapshot


def test_missing_snapshot_returns_none():

    registry = GovernanceSnapshotRegistry()

    assert registry.get(
        "missing"
    ) is None


def test_registry_lists_snapshots():

    registry = GovernanceSnapshotRegistry()

    registry.add(
        HistoricalGovernanceSnapshot(
            snapshot_id="snap-001",
            policy_version="trust-policy:v1",
            authority_id="auth-001",
        )
    )

    registry.add(
        HistoricalGovernanceSnapshot(
            snapshot_id="snap-002",
            policy_version="trust-policy:v2",
            authority_id="auth-002",
        )
    )

    assert registry.snapshot_ids() == [
        "snap-001",
        "snap-002",
    ]
