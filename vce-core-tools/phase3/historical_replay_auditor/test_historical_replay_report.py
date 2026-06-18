from phase3.historical_replay_auditor.replay_certification import (
    ReplayCertification,
)

from phase3.historical_replay_auditor.historical_replay_report import (
    HistoricalReplayReport,
)


def test_report_contains_status():

    certification = ReplayCertification(
        status="PASS",
        certified=True,
    )

    report = HistoricalReplayReport(
        certification
    )

    assert report.status() == "PASS"


def test_report_contains_certified_flag():

    certification = ReplayCertification(
        status="PASS",
        certified=True,
    )

    report = HistoricalReplayReport(
        certification
    )

    assert report.certified() is True


def test_report_serializes():

    certification = ReplayCertification(
        status="PASS",
        certified=True,
    )

    report = HistoricalReplayReport(
        certification
    )

    assert report.to_dict() == {
        "status": "PASS",
        "certified": True,
    }
