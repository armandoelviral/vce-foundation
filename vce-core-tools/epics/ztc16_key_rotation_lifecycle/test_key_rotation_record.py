from epics.ztc16_key_rotation_lifecycle.key_rotation_record import (
    KeyRotationRecord,
)


def test_record_contains_witness_id():

    record = KeyRotationRecord(
        witness_id="witness-001",
        old_key_id="key-active-001",
        new_key_id="key-next-001",
        reason="scheduled_rotation",
    )

    assert record.witness_id == "witness-001"


def test_record_contains_old_and_new_keys():

    record = KeyRotationRecord(
        witness_id="witness-001",
        old_key_id="key-active-001",
        new_key_id="key-next-001",
        reason="scheduled_rotation",
    )

    assert record.old_key_id == "key-active-001"
    assert record.new_key_id == "key-next-001"


def test_record_serializes():

    record = KeyRotationRecord(
        witness_id="witness-001",
        old_key_id="key-active-001",
        new_key_id="key-next-001",
        reason="scheduled_rotation",
    )

    assert record.to_dict() == {
        "witness_id": "witness-001",
        "old_key_id": "key-active-001",
        "new_key_id": "key-next-001",
        "reason": "scheduled_rotation",
    }
