from epics.ztc15_witness_suspension_recovery.recovery_record import (
    RecoveryRecord,
)


def test_record_contains_witness_id():

    record = RecoveryRecord(
        witness_id="witness-001",
        recovery_reason="key_rotation_completed",
    )

    assert record.witness_id == "witness-001"


def test_record_contains_recovery_reason():

    record = RecoveryRecord(
        witness_id="witness-001",
        recovery_reason="key_rotation_completed",
    )

    assert (
        record.recovery_reason
        == "key_rotation_completed"
    )


def test_record_serializes():

    record = RecoveryRecord(
        witness_id="witness-001",
        recovery_reason="key_rotation_completed",
    )

    assert record.to_dict() == {
        "witness_id": "witness-001",
        "recovery_reason": "key_rotation_completed",
    }
