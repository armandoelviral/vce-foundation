from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)

from phase3.replay_certification_engine.replay_certificate_registry import (
    ReplayCertificateRegistry,
)

from phase3.replay_certification_engine.certificate_report import (
    CertificateReport,
)


def test_report_contains_certificate_count():

    registry = ReplayCertificateRegistry()

    registry.add(
        ReplayCertificateRecord(
            certificate_id="cert-001",
            replay_id="replay-001",
            status="PASS",
        )
    )

    report = CertificateReport(
        registry
    )

    assert report.certificate_count() == 1


def test_report_lists_certificate_ids():

    registry = ReplayCertificateRegistry()

    registry.add(
        ReplayCertificateRecord(
            certificate_id="cert-001",
            replay_id="replay-001",
            status="PASS",
        )
    )

    registry.add(
        ReplayCertificateRecord(
            certificate_id="cert-002",
            replay_id="replay-002",
            status="FAIL",
        )
    )

    report = CertificateReport(
        registry
    )

    assert report.certificate_ids() == [
        "cert-001",
        "cert-002",
    ]


def test_report_serializes():

    registry = ReplayCertificateRegistry()

    registry.add(
        ReplayCertificateRecord(
            certificate_id="cert-001",
            replay_id="replay-001",
            status="PASS",
        )
    )

    report = CertificateReport(
        registry
    )

    assert report.to_dict() == {
        "certificate_count": 1,
        "certificate_ids": [
            "cert-001",
        ],
    }
