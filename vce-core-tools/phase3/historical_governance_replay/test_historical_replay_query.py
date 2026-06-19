from phase3.historical_governance_replay.historical_governance_snapshot import (
    HistoricalGovernanceSnapshot,
)

from phase3.historical_governance_replay.governance_snapshot_registry import (
    GovernanceSnapshotRegistry,
)

from phase3.historical_governance_replay.historical_replay_query import (
    HistoricalReplayQuery,
)


def test_query_returns_snapshot():

    registry = GovernanceSnapshotRegistry()

    snapshot = HistoricalGovernanceSnapshot(
        snapshot_id="snap-001",
        policy_version="trust-policy:v2",
        authority_id="auth-001",
    )

    registry.add(snapshot)

    query = HistoricalReplayQuery(
        registry
    )

    result = query.by_id(
        "snap-001"
    )

    assert result == snapshot


def test_query_returns_none_for_missing():

    registry = GovernanceSnapshotRegistry()

    query = HistoricalReplayQuery(
        registry
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_policy_version():

    registry = GovernanceSnapshotRegistry()

    snapshot = HistoricalGovernanceSnapshot(
        snapshot_id="snap-001",
        policy_version="trust-policy:v2",
        authority_id="auth-001",
    )

    registry.add(snapshot)

    query = HistoricalReplayQuery(
        registry
    )

    result = query.by_id(
        "snap-001"
    )

    assert (
        result.policy_version
        == "trust-policy:v2"
    )
