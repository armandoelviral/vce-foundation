from phase2.provenance_persistence.provenance_record import (
    ProvenanceRecord,
)

from phase2.provenance_persistence.provenance_verifier import (
    ProvenanceVerifier,
)


def test_verifier_accepts_matching_hash():

    record = ProvenanceRecord(
        subject_id="artifact-001",
        origin_id="execution-001",
        provenance_hash="hash-001",
    )

    assert (
        ProvenanceVerifier.verify(
            record,
            expected_hash="hash-001",
        )
        is True
    )


def test_verifier_rejects_mismatch():

    record = ProvenanceRecord(
        subject_id="artifact-001",
        origin_id="execution-001",
        provenance_hash="hash-001",
    )

    assert (
        ProvenanceVerifier.verify(
            record,
            expected_hash="hash-999",
        )
        is False
    )


def test_verifier_rejects_empty_hash():

    record = ProvenanceRecord(
        subject_id="artifact-001",
        origin_id="execution-001",
        provenance_hash="",
    )

    assert (
        ProvenanceVerifier.verify(
            record,
            expected_hash="",
        )
        is False
    )
