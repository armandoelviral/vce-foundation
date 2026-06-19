from phase3.cryptographic_replay_report.cryptographic_replay_report_record import (
    CryptographicReplayReportRecord,
)

from phase3.cryptographic_replay_report.report_query import (
    ReportQuery,
)


def test_query_returns_report():

    report = CryptographicReplayReportRecord(
        report_id="report-001",
        certificate_id="cert-001",
        status="PASS",
    )

    query = ReportQuery(
        {
            "report-001": report
        }
    )

    result = query.by_id(
        "report-001"
    )

    assert result == report


def test_query_returns_none_for_missing():

    query = ReportQuery(
        {}
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_status():

    report = CryptographicReplayReportRecord(
        report_id="report-001",
        certificate_id="cert-001",
        status="PASS",
    )

    query = ReportQuery(
        {
            "report-001": report
        }
    )

    result = query.by_id(
        "report-001"
    )

    assert result.status == "PASS"
