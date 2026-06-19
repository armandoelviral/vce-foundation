from phase3.cryptographic_replay_report.cryptographic_replay_report_record import (
    CryptographicReplayReportRecord,
)

from phase3.cryptographic_replay_report.report_attestation import (
    ReportAttestation,
)


def test_attestation_subject():

    report = CryptographicReplayReportRecord(
        report_id="report-001",
        certificate_id="cert-001",
        status="PASS",
    )

    attestation = (
        ReportAttestation.attest(
            attestation_id="att-001",
            report=report,
        )
    )

    assert attestation.subject == "cryptographic_replay_report"


def test_attestation_uses_report_id():

    report = CryptographicReplayReportRecord(
        report_id="report-001",
        certificate_id="cert-001",
        status="PASS",
    )

    attestation = (
        ReportAttestation.attest(
            attestation_id="att-001",
            report=report,
        )
    )

    assert (
        attestation.evidence_hash
        == "report-001"
    )


def test_attestation_preserves_id():

    report = CryptographicReplayReportRecord(
        report_id="report-001",
        certificate_id="cert-001",
        status="PASS",
    )

    attestation = (
        ReportAttestation.attest(
            attestation_id="att-001",
            report=report,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
