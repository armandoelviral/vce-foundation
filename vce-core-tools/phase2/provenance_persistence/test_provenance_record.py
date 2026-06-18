from phase2.provenance_persistence.provenance_record import (
    ProvenanceRecord,
)


def test_record_contains_subject_id():

    record = ProvenanceRecord(
        subject_id="artifact-001",
        origin_id="execution-001",
        provenance_hash="hash-001",
    )

    assert record.subject_id == "artifact-001"


def test_record_contains_origin_id():

    record = ProvenanceRecord(
        subject_id="artifact-001",
        origin_id="execution-001",
        provenance_hash="hash-001",
    )

    assert record.origin_id == "execution-001"


def test_record_contains_provenance_hash():

    record = ProvenanceRecord(
        subject_id="artifact-001",
        origin_id="execution-001",
        provenance_hash="hash-001",
    )

    assert record.provenance_hash == "hash-001"


def test_record_serializes():

    record = ProvenanceRecord(
        subject_id="artifact-001",
        origin_id="execution-001",
        provenance_hash="hash-001",
    )

    assert record.to_dict() == {
        "subject_id": "artifact-001",
        "origin_id": "execution-001",
        "provenance_hash": "hash-001",
    }
