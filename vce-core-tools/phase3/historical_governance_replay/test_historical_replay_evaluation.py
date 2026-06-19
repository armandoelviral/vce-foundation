from phase3.historical_governance_replay.historical_governance_snapshot import (
    HistoricalGovernanceSnapshot,
)

from phase3.historical_governance_replay.historical_replay_evaluation import (
    HistoricalReplayEvaluation,
)


def test_complete_snapshot_is_replayable():

    snapshot = HistoricalGovernanceSnapshot(
        snapshot_id="snap-001",
        policy_version="trust-policy:v2",
        authority_id="auth-001",
    )

    result = HistoricalReplayEvaluation.evaluate(
        snapshot
    )

    assert result is True


def test_missing_policy_version_is_not_replayable():

    snapshot = HistoricalGovernanceSnapshot(
        snapshot_id="snap-001",
        policy_version="",
        authority_id="auth-001",
    )

    result = HistoricalReplayEvaluation.evaluate(
        snapshot
    )

    assert result is False


def test_missing_authority_is_not_replayable():

    snapshot = HistoricalGovernanceSnapshot(
        snapshot_id="snap-001",
        policy_version="trust-policy:v2",
        authority_id="",
    )

    result = HistoricalReplayEvaluation.evaluate(
        snapshot
    )

    assert result is False
