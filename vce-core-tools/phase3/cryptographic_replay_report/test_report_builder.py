from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)

from phase3.cryptographic_replay_report.report_builder import (
    ReportBuilder,
)


def test_builder_creates_report():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    report = ReportBuilder.build(
        report_id="report-001",
        certificate=certificate,
    )

    assert report.report_id == "report-001"


def test_builder_preserves_certificate_id():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    report = ReportBuilder.build(
        report_id="report-001",
        certificate=certificate,
    )

    assert report.certificate_id == "cert-001"


def test_builder_preserves_status():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    report = ReportBuilder.build(
        report_id="report-001",
        certificate=certificate,
    )

    assert report.status == "PASS"
