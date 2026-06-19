from phase3.certificate_transparency.transparency_certificate_record import (
    TransparencyCertificateRecord,
)

from phase3.certificate_transparency.transparency_log import (
    TransparencyLog,
)


def test_log_starts_empty():

    log = TransparencyLog()

    assert log.count() == 0


def test_log_accepts_entry():

    log = TransparencyLog()

    entry = TransparencyCertificateRecord(
        entry_id="entry-001",
        certificate_id="cert-001",
    )

    log.add(
        entry
    )

    assert log.count() == 1


def test_log_returns_entry():

    log = TransparencyLog()

    entry = TransparencyCertificateRecord(
        entry_id="entry-001",
        certificate_id="cert-001",
    )

    log.add(
        entry
    )

    recovered = log.get(
        "entry-001"
    )

    assert recovered == entry


def test_missing_entry_returns_none():

    log = TransparencyLog()

    assert log.get(
        "missing"
    ) is None
