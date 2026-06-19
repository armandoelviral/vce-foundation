from phase3.historical_governance_replay.historical_governance_snapshot import (
    HistoricalGovernanceSnapshot,
)

from phase3.historical_governance_replay.historical_replay_attestation import (
    HistoricalReplayAttestation,
)


def test_attestation_subject():

    snapshot = HistoricalGovernanceSnapshot(
        snapshot_id="snap-001",
        policy_version="trust-policy:v2",
        authority_id="auth-001",
    )

    attestation = (
        HistoricalReplayAttestation.attest(
            attestation_id="att-001",
            snapshot=snapshot,
        )
    )

    assert (
        attestation.subject
        == "historical_governance_snapshot"
    )


def test_attestation_uses_snapshot_id():

    snapshot = HistoricalGovernanceSnapshot(
        snapshot_id="snap-001",
        policy_version="trust-policy:v2",
        authority_id="auth-001",
    )

    attestation = (
        HistoricalReplayAttestation.attest(
            attestation_id="att-001",
            snapshot=snapshot,
        )
    )

    assert (
        attestation.evidence_hash
        == "snap-001"
    )


def test_attestation_preserves_id():

    snapshot = HistoricalGovernanceSnapshot(
        snapshot_id="snap-001",
        policy_version="trust-policy:v2",
        authority_id="auth-001",
    )

    attestation = (
        HistoricalReplayAttestation.attest(
            attestation_id="att-001",
            snapshot=snapshot,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
