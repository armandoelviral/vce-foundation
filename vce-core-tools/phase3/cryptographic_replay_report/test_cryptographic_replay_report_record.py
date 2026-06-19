from phase3.cryptographic_replay_report.cryptographic_replay_report_record import (
    CryptographicReplayReportRecord,
)


def test_report_contains_report_id():

    report = CryptographicReplayReportRecord(
        report_id="report-001",
        certificate_id="cert-001",
        status="PASS",
    )

    assert report.report_id == "report-001"


def test_report_contains_certificate_id():

    report = CryptographicReplayReportRecord(
        report_id="report-001",
        certificate_id="cert-001",
        status="PASS",
    )

    assert report.certificate_id == "cert-001"


def test_report_contains_status():

    report = CryptographicReplayReportRecord(
        report_id="report-001",
        certificate_id="cert-001",
        status="PASS",
    )

    assert report.status == "PASS"


def test_report_serializes():

    report = CryptographicReplayReportRecord(
        report_id="report-001",
        certificate_id="cert-001",
        status="PASS",
    )

    assert report.to_dict() == {
        "report_id": "report-001",
        "certificate_id": "cert-001",
        "status": "PASS",
    }
