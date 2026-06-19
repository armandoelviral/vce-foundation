from phase3.historical_governance_replay.historical_governance_snapshot import (
    HistoricalGovernanceSnapshot,
)

from phase3.historical_governance_replay.historical_replay_report import (
    HistoricalReplayReport,
)


def test_report_contains_snapshot_count():

    report = HistoricalReplayReport(
        {
            "snap-001":
                HistoricalGovernanceSnapshot(
                    snapshot_id="snap-001",
                    policy_version="trust-policy:v1",
                    authority_id="auth-001",
                )
        }
    )

    assert report.snapshot_count() == 1


def test_report_lists_snapshot_ids():

    report = HistoricalReplayReport(
        {
            "snap-001":
                HistoricalGovernanceSnapshot(
                    snapshot_id="snap-001",
                    policy_version="trust-policy:v1",
                    authority_id="auth-001",
                ),

            "snap-002":
                HistoricalGovernanceSnapshot(
                    snapshot_id="snap-002",
                    policy_version="trust-policy:v2",
                    authority_id="auth-002",
                ),
        }
    )

    assert report.snapshot_ids() == [
        "snap-001",
        "snap-002",
    ]


def test_report_serializes():

    report = HistoricalReplayReport(
        {
            "snap-001":
                HistoricalGovernanceSnapshot(
                    snapshot_id="snap-001",
                    policy_version="trust-policy:v1",
                    authority_id="auth-001",
                )
        }
    )

    assert report.to_dict() == {
        "snapshot_count": 1,
        "snapshot_ids": [
            "snap-001",
        ],
    }
