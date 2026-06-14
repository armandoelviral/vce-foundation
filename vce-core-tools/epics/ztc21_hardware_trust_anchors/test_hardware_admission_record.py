from epics.ztc21_hardware_trust_anchors.hardware_admission_record import (
    HardwareAdmissionRecord,
)


def test_record_contains_provider():

    record = HardwareAdmissionRecord(
        provider="aws",
        admitted=True,
        reason="hardware_anchor_verified",
    )

    assert record.provider == "aws"


def test_record_contains_admission_status():

    record = HardwareAdmissionRecord(
        provider="aws",
        admitted=True,
        reason="hardware_anchor_verified",
    )

    assert record.admitted is True


def test_record_serializes():

    record = HardwareAdmissionRecord(
        provider="aws",
        admitted=False,
        reason="hardware_anchor_failed",
    )

    assert record.to_dict() == {
        "provider": "aws",
        "admitted": False,
        "reason": "hardware_anchor_failed",
    }
