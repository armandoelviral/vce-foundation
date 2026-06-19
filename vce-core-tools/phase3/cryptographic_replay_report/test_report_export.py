from phase3.cryptographic_replay_report.cryptographic_replay_report_record import (
    CryptographicReplayReportRecord,
)

from phase3.cryptographic_replay_report.report_export import (
    ReportExport,
)


def test_export_contains_report_id():

    report = CryptographicReplayReportRecord(
        report_id="report-001",
        certificate_id="cert-001",
        status="PASS",
    )

    exported = ReportExport.export(
        report
    )

    assert (
        exported["report_id"]
        == "report-001"
    )


def test_export_contains_certificate_id():

    report = CryptographicReplayReportRecord(
        report_id="report-001",
        certificate_id="cert-001",
        status="PASS",
    )

    exported = ReportExport.export(
        report
    )

    assert (
        exported["certificate_id"]
        == "cert-001"
    )


def test_export_contains_status():

    report = CryptographicReplayReportRecord(
        report_id="report-001",
        certificate_id="cert-001",
        status="PASS",
    )

    exported = ReportExport.export(
        report
    )

    assert (
        exported["status"]
        == "PASS"
    )
