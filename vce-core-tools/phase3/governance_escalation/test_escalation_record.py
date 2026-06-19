from phase3.governance_escalation.escalation_record import (
    EscalationRecord,
)


def test_record_contains_id():

    record = EscalationRecord(
        escalation_id="esc-001",
        reason="quorum_failure",
        severity="HIGH",
    )

    assert (
        record.escalation_id
        == "esc-001"
    )


def test_record_contains_reason():

    record = EscalationRecord(
        escalation_id="esc-001",
        reason="quorum_failure",
        severity="HIGH",
    )

    assert (
        record.reason
        == "quorum_failure"
    )


def test_record_contains_severity():

    record = EscalationRecord(
        escalation_id="esc-001",
        reason="quorum_failure",
        severity="HIGH",
    )

    assert (
        record.severity
        == "HIGH"
    )


def test_record_serializes():

    record = EscalationRecord(
        escalation_id="esc-001",
        reason="quorum_failure",
        severity="HIGH",
    )

    assert record.to_dict() == {
        "escalation_id": "esc-001",
        "reason": "quorum_failure",
        "severity": "HIGH",
    }
