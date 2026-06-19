from phase3.certificate_transparency.transparency_certificate_record import (
    TransparencyCertificateRecord,
)

from phase3.certificate_transparency.transparency_log import (
    TransparencyLog,
)

from phase3.certificate_transparency.transparency_report import (
    TransparencyReport,
)


def test_report_contains_entry_count():

    log = TransparencyLog()

    log.add(
        TransparencyCertificateRecord(
            entry_id="entry-001",
            certificate_id="cert-001",
        )
    )

    report = TransparencyReport(
        log
    )

    assert report.entry_count() == 1


def test_report_lists_entry_ids():

    log = TransparencyLog()

    log.add(
        TransparencyCertificateRecord(
            entry_id="entry-001",
            certificate_id="cert-001",
        )
    )

    log.add(
        TransparencyCertificateRecord(
            entry_id="entry-002",
            certificate_id="cert-002",
        )
    )

    report = TransparencyReport(
        log
    )

    assert report.entry_ids() == [
        "entry-001",
        "entry-002",
    ]


def test_report_serializes():

    log = TransparencyLog()

    log.add(
        TransparencyCertificateRecord(
            entry_id="entry-001",
            certificate_id="cert-001",
        )
    )

    report = TransparencyReport(
        log
    )

    assert report.to_dict() == {
        "entry_count": 1,
        "entry_ids": [
            "entry-001",
        ],
    }
