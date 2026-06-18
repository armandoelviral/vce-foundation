from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase2.attestation_persistence.attestation_report import (
    AttestationReport,
)


def test_report_contains_total_attestations():

    records = [
        AttestationRecord(
            attestation_id="att-001",
            subject="runtime-state",
            evidence_hash="hash-001",
        ),
        AttestationRecord(
            attestation_id="att-002",
            subject="recovery",
            evidence_hash="hash-002",
        ),
    ]

    report = AttestationReport(records)

    assert report.total_attestations() == 2


def test_report_lists_subjects():

    records = [
        AttestationRecord(
            attestation_id="att-001",
            subject="runtime-state",
            evidence_hash="hash-001",
        ),
        AttestationRecord(
            attestation_id="att-002",
            subject="recovery",
            evidence_hash="hash-002",
        ),
    ]

    report = AttestationReport(records)

    assert report.subjects() == [
        "runtime-state",
        "recovery",
    ]


def test_report_serializes():

    records = [
        AttestationRecord(
            attestation_id="att-001",
            subject="runtime-state",
            evidence_hash="hash-001",
        )
    ]

    report = AttestationReport(records)

    assert report.to_dict() == {
        "total_attestations": 1,
        "subjects": [
            "runtime-state",
        ],
    }
