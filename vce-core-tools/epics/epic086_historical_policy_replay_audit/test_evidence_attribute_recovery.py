from epics.epic086_historical_policy_replay_audit.evidence_attribute_recovery import (
    EvidenceAttributeRecovery,
)


def build_ledger():

    return {
        "evidence-hash-001": {
            "evidence_hash": "evidence-hash-001",
            "policy_id": "clinical-admission-policy",
            "policy_version": "2.0.0",
            "execution_attributes": {
                "process_id": "tumor-classifier-v3",
                "cps_level": 5,
                "region": "us-east-1",
                "environment": "production",
            },
            "original_decision": "ADMIT",
        }
    }


def test_recovery_returns_evidence_attributes():

    recovery = EvidenceAttributeRecovery(
        build_ledger()
    )

    evidence = recovery.recover(
        "evidence-hash-001"
    )

    assert evidence["evidence_hash"] == "evidence-hash-001"
    assert evidence["policy_id"] == "clinical-admission-policy"
    assert evidence["policy_version"] == "2.0.0"


def test_recovery_returns_execution_attributes():

    recovery = EvidenceAttributeRecovery(
        build_ledger()
    )

    evidence = recovery.recover(
        "evidence-hash-001"
    )

    attributes = evidence["execution_attributes"]

    assert attributes["process_id"] == "tumor-classifier-v3"
    assert attributes["cps_level"] == 5
    assert attributes["environment"] == "production"


def test_recovery_returns_original_decision():

    recovery = EvidenceAttributeRecovery(
        build_ledger()
    )

    evidence = recovery.recover(
        "evidence-hash-001"
    )

    assert evidence["original_decision"] == "ADMIT"


def test_recovery_returns_none_for_unknown_evidence():

    recovery = EvidenceAttributeRecovery(
        build_ledger()
    )

    assert recovery.recover(
        "unknown-evidence"
    ) is None
