from phase3.cryptographic_replay_report.report_signature import (
    ReportSignature,
)


def test_signature_contains_report_id():

    signature = ReportSignature(
        report_id="report-001",
        signature="sig-001",
    )

    assert signature.report_id == "report-001"


def test_signature_contains_signature():

    signature = ReportSignature(
        report_id="report-001",
        signature="sig-001",
    )

    assert signature.signature == "sig-001"


def test_signature_serializes():

    signature = ReportSignature(
        report_id="report-001",
        signature="sig-001",
    )

    assert signature.to_dict() == {
        "report_id": "report-001",
        "signature": "sig-001",
    }
