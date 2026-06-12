from epics.epic085_policy_authority_layer.policy_registry import (
    GovernancePolicy,
    PolicyRegistry,
)

from epics.epic086_historical_policy_replay_audit.replay_request import (
    ReplayRequest,
)

from epics.epic086_historical_policy_replay_audit.evidence_attribute_recovery import (
    EvidenceAttributeRecovery,
)

from epics.epic086_historical_policy_replay_audit.version_pinned_policy_resolution import (
    VersionPinnedPolicyResolution,
)

from epics.epic086_historical_policy_replay_audit.witness_replay_vote import (
    WitnessReplayVote,
)

from epics.epic086_historical_policy_replay_audit.replay_result_comparator import (
    ReplayResultComparator,
)

from epics.epic086_historical_policy_replay_audit.cryptographic_audit_report import (
    build_audit_report,
)


def build_registry():

    registry = PolicyRegistry()

    registry.register(
        GovernancePolicy(
            policy_id="clinical-admission-policy",
            policy_version="2.0.0",
            policy_hash="policy-hash-v2",
            active=True,
        )
    )

    return registry


def build_evidence_ledger():

    return {
        "evidence-hash-001": {
            "evidence_hash": "evidence-hash-001",
            "policy_id": "clinical-admission-policy",
            "policy_version": "2.0.0",
            "execution_attributes": {
                "process_id": "tumor-classifier-v3",
                "cps_level": 5,
            },
            "original_decision": "ADMIT",
        }
    }


def test_end_to_end_historical_replay_flow():

    request = ReplayRequest(
        evidence_hash="evidence-hash-001",
        policy_id="clinical-admission-policy",
        policy_version="2.0.0",
        requested_by="auditor",
        requested_at="2026-06-10T00:00:00Z",
    )

    recovery = EvidenceAttributeRecovery(
        build_evidence_ledger()
    )

    evidence = recovery.recover(
        request.evidence_hash
    )

    resolver = VersionPinnedPolicyResolution(
        build_registry()
    )

    policy = resolver.resolve(
        evidence["policy_id"],
        evidence["policy_version"],
    )

    assert policy is not None

    vote = WitnessReplayVote(
        witness_id="witness-001",
        evidence_hash=evidence["evidence_hash"],
        policy_id=evidence["policy_id"],
        policy_version=evidence["policy_version"],
        replay_result="REPLAY_MATCH",
        observed_at="2026-06-10T00:01:00Z",
    )

    comparator = ReplayResultComparator()

    comparison = comparator.compare(
        original_decision=evidence["original_decision"],
        replay_decision="ADMIT",
    )

    report = build_audit_report(
        evidence,
        comparison,
    )

    assert vote.replay_result == "REPLAY_MATCH"

    assert (
        report.replay_result
        == "REPLAY_MATCH"
    )

    assert report.verified is True

    assert (
        report.policy_version
        == "2.0.0"
    )


def test_end_to_end_historical_replay_detects_mismatch():

    recovery = EvidenceAttributeRecovery(
        build_evidence_ledger()
    )

    evidence = recovery.recover(
        "evidence-hash-001"
    )

    comparator = ReplayResultComparator()

    comparison = comparator.compare(
        original_decision=evidence["original_decision"],
        replay_decision="REJECT",
    )

    report = build_audit_report(
        evidence,
        comparison,
    )

    assert (
        report.replay_result
        == "REPLAY_MISMATCH"
    )

    assert report.verified is False
