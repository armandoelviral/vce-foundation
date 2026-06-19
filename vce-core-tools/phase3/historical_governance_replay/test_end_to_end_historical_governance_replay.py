from phase3.historical_governance_replay.historical_governance_snapshot import (
    HistoricalGovernanceSnapshot,
)

from phase3.historical_governance_replay.governance_snapshot_registry import (
    GovernanceSnapshotRegistry,
)

from phase3.historical_governance_replay.historical_replay_evaluation import (
    HistoricalReplayEvaluation,
)

from phase3.historical_governance_replay.historical_replay_decision import (
    HistoricalReplayDecision,
)

from phase3.historical_governance_replay.historical_replay_query import (
    HistoricalReplayQuery,
)

from phase3.historical_governance_replay.historical_replay_report import (
    HistoricalReplayReport,
)

from phase3.historical_governance_replay.historical_replay_attestation import (
    HistoricalReplayAttestation,
)


def test_end_to_end_historical_governance_replay():

    registry = GovernanceSnapshotRegistry()

    snapshot = HistoricalGovernanceSnapshot(
        snapshot_id="snap-001",
        policy_version="trust-policy:v2",
        authority_id="auth-001",
    )

    registry.add(snapshot)

    evaluation = HistoricalReplayEvaluation.evaluate(
        snapshot
    )

    assert evaluation is True

    decision = HistoricalReplayDecision.from_evaluation(
        evaluation
    )

    assert decision.status == "REPLAY"

    query = HistoricalReplayQuery(
        registry
    )

    recovered = query.by_id(
        "snap-001"
    )

    assert recovered == snapshot

    report = HistoricalReplayReport(
        {
            "snap-001": recovered
        }
    )

    assert report.snapshot_count() == 1
    assert report.snapshot_ids() == [
        "snap-001",
    ]

    attestation = HistoricalReplayAttestation.attest(
        attestation_id="att-001",
        snapshot=snapshot,
    )

    assert (
        attestation.subject
        == "historical_governance_snapshot"
    )

    assert (
        attestation.evidence_hash
        == "snap-001"
    )
