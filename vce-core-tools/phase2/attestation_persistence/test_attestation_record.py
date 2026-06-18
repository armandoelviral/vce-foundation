from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)


def test_record_contains_attestation_id():

    record = AttestationRecord(
        attestation_id="att-001",
        subject="runtime-state",
        evidence_hash="hash-001",
    )

    assert record.attestation_id == "att-001"


def test_record_contains_subject():

    record = AttestationRecord(
        attestation_id="att-001",
        subject="runtime-state",
        evidence_hash="hash-001",
    )

    assert record.subject == "runtime-state"


def test_record_contains_evidence_hash():

    record = AttestationRecord(
        attestation_id="att-001",
        subject="runtime-state",
        evidence_hash="hash-001",
    )

    assert record.evidence_hash == "hash-001"


def test_record_serializes():

    record = AttestationRecord(
        attestation_id="att-001",
        subject="runtime-state",
        evidence_hash="hash-001",
    )

    assert record.to_dict() == {
        "attestation_id": "att-001",
        "subject": "runtime-state",
        "evidence_hash": "hash-001",
    }
