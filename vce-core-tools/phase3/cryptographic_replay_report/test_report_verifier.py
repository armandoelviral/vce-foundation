from phase3.cryptographic_replay_report.cryptographic_replay_report_record import (
    CryptographicReplayReportRecord,
)

from phase3.cryptographic_replay_report.report_verifier import (
    ReportVerifier,
)


def test_valid_report_passes():

    report = CryptographicReplayReportRecord(
        report_id="report-001",
        certificate_id="cert-001",
        status="PASS",
    )

    assert (
        ReportVerifier.verify(
            report
        )
        is True
    )


def test_missing_report_id_fails():

    report = CryptographicReplayReportRecord(
        report_id="",
        certificate_id="cert-001",
        status="PASS",
    )

    assert (
        ReportVerifier.verify(
            report
        )
        is False
    )


def test_missing_certificate_id_fails():

    report = CryptographicReplayReportRecord(
        report_id="report-001",
        certificate_id="",
        status="PASS",
    )

    assert (
        ReportVerifier.verify(
            report
        )
        is False
    )


def test_missing_status_fails():

    report = CryptographicReplayReportRecord(
        report_id="report-001",
        certificate_id="cert-001",
        status="",
    )

    assert (
        ReportVerifier.verify(
            report
        )
        is False
    )
