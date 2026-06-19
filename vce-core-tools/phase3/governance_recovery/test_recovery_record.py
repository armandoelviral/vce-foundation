from phase3.governance_recovery.recovery_record import (
    RecoveryRecord,
)


def test_record_contains_id():

    record = RecoveryRecord(
        recovery_id="rec-001",
        incident_id="esc-001",
        recovery_reason="manual_remediation",
    )

    assert (
        record.recovery_id
        == "rec-001"
    )


def test_record_contains_incident_id():

    record = RecoveryRecord(
        recovery_id="rec-001",
        incident_id="esc-001",
        recovery_reason="manual_remediation",
    )

    assert (
        record.incident_id
        == "esc-001"
    )


def test_record_contains_reason():

    record = RecoveryRecord(
        recovery_id="rec-001",
        incident_id="esc-001",
        recovery_reason="manual_remediation",
    )

    assert (
        record.recovery_reason
        == "manual_remediation"
    )


def test_record_serializes():

    record = RecoveryRecord(
        recovery_id="rec-001",
        incident_id="esc-001",
        recovery_reason="manual_remediation",
    )

    assert record.to_dict() == {
        "recovery_id": "rec-001",
        "incident_id": "esc-001",
        "recovery_reason":
            "manual_remediation",
    }
