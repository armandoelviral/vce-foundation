from epics.ztc20_confidential_compute_attestation.attestation_admission_record import (
    AttestationAdmissionRecord,
)


def test_record_contains_witness_id():

    record = AttestationAdmissionRecord(
        witness_id="witness-001",
        admitted=True,
        reason="attestation_verified",
    )

    assert record.witness_id == "witness-001"


def test_record_contains_admission_status():

    record = AttestationAdmissionRecord(
        witness_id="witness-001",
        admitted=True,
        reason="attestation_verified",
    )

    assert record.admitted is True


def test_record_serializes():

    record = AttestationAdmissionRecord(
        witness_id="witness-001",
        admitted=False,
        reason="attestation_failed",
    )

    assert record.to_dict() == {
        "witness_id": "witness-001",
        "admitted": False,
        "reason": "attestation_failed",
    }
