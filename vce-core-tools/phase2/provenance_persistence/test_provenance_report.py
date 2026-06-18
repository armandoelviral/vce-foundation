from phase2.provenance_persistence.provenance_record import (
    ProvenanceRecord,
)

from phase2.provenance_persistence.provenance_report import (
    ProvenanceReport,
)


def test_report_contains_total_records():

    records = [
        ProvenanceRecord(
            subject_id="artifact-001",
            origin_id="execution-001",
            provenance_hash="hash-001",
        ),
        ProvenanceRecord(
            subject_id="artifact-002",
            origin_id="execution-002",
            provenance_hash="hash-002",
        ),
    ]

    report = ProvenanceReport(records)

    assert report.total_records() == 2


def test_report_lists_subject_ids():

    records = [
        ProvenanceRecord(
            subject_id="artifact-001",
            origin_id="execution-001",
            provenance_hash="hash-001",
        ),
        ProvenanceRecord(
            subject_id="artifact-002",
            origin_id="execution-002",
            provenance_hash="hash-002",
        ),
    ]

    report = ProvenanceReport(records)

    assert report.subject_ids() == [
        "artifact-001",
        "artifact-002",
    ]


def test_report_serializes():

    records = [
        ProvenanceRecord(
            subject_id="artifact-001",
            origin_id="execution-001",
            provenance_hash="hash-001",
        )
    ]

    report = ProvenanceReport(records)

    assert report.to_dict() == {
        "total_records": 1,
        "subject_ids": [
            "artifact-001",
        ],
    }
