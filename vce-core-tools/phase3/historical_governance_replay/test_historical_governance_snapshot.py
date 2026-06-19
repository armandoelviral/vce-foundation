from phase3.historical_governance_replay.historical_governance_snapshot import (
    HistoricalGovernanceSnapshot,
)


def test_contains_snapshot_id():

    snapshot = HistoricalGovernanceSnapshot(
        snapshot_id="snap-001",
        policy_version="trust-policy:v2",
        authority_id="auth-001",
    )

    assert (
        snapshot.snapshot_id
        == "snap-001"
    )


def test_contains_policy_version():

    snapshot = HistoricalGovernanceSnapshot(
        snapshot_id="snap-001",
        policy_version="trust-policy:v2",
        authority_id="auth-001",
    )

    assert (
        snapshot.policy_version
        == "trust-policy:v2"
    )


def test_contains_authority_id():

    snapshot = HistoricalGovernanceSnapshot(
        snapshot_id="snap-001",
        policy_version="trust-policy:v2",
        authority_id="auth-001",
    )

    assert (
        snapshot.authority_id
        == "auth-001"
    )


def test_serializes():

    snapshot = HistoricalGovernanceSnapshot(
        snapshot_id="snap-001",
        policy_version="trust-policy:v2",
        authority_id="auth-001",
    )

    assert snapshot.to_dict() == {
        "snapshot_id": "snap-001",
        "policy_version": "trust-policy:v2",
        "authority_id": "auth-001",
    }
