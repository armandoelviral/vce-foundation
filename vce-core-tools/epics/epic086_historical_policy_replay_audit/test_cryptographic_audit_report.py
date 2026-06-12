from epics.epic086_historical_policy_replay_audit.cryptographic_audit_report import (
    build_audit_report,
)


def build_evidence():

    return {
        "evidence_hash": "evidence-hash-001",
        "policy_id": "clinical-admission-policy",
        "policy_version": "2.0.0",
        "original_decision": "ADMIT",
    }


def test_audit_report_accepts_matching_replay():

    comparison = {
        "result": "REPLAY_MATCH",
        "original_decision": "ADMIT",
        "replay_decision": "ADMIT",
    }

    report = build_audit_report(
        build_evidence(),
        comparison,
    )

    assert report.verified is True
    assert report.replay_result == "REPLAY_MATCH"


def test_audit_report_rejects_mismatched_replay():

    comparison = {
        "result": "REPLAY_MISMATCH",
        "original_decision": "ADMIT",
        "replay_decision": "REJECT",
    }

    report = build_audit_report(
        build_evidence(),
        comparison,
    )

    assert report.verified is False
    assert report.replay_result == "REPLAY_MISMATCH"


def test_audit_report_contains_policy_version():

    comparison = {
        "result": "REPLAY_MATCH",
        "original_decision": "ADMIT",
        "replay_decision": "ADMIT",
    }

    report = build_audit_report(
        build_evidence(),
        comparison,
    )

    assert report.policy_id == "clinical-admission-policy"
    assert report.policy_version == "2.0.0"


def test_audit_report_serializes():

    comparison = {
        "result": "REPLAY_MATCH",
        "original_decision": "ADMIT",
        "replay_decision": "ADMIT",
    }

    report = build_audit_report(
        build_evidence(),
        comparison,
    )

    payload = report.to_dict()

    assert payload["evidence_hash"] == "evidence-hash-001"
    assert payload["policy_version"] == "2.0.0"
    assert payload["verified"] is True
