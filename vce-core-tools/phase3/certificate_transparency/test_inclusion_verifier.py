from phase3.certificate_transparency.transparency_certificate_record import (
    TransparencyCertificateRecord,
)

from phase3.certificate_transparency.transparency_log import (
    TransparencyLog,
)

from phase3.certificate_transparency.inclusion_verifier import (
    InclusionVerifier,
)


def test_existing_entry_verifies():

    log = TransparencyLog()

    entry = TransparencyCertificateRecord(
        entry_id="entry-001",
        certificate_id="cert-001",
    )

    log.add(
        entry
    )

    assert (
        InclusionVerifier.verify(
            log,
            "entry-001",
        )
        is True
    )


def test_missing_entry_fails():

    log = TransparencyLog()

    assert (
        InclusionVerifier.verify(
            log,
            "missing",
        )
        is False
    )


def test_multiple_entries_supported():

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

    assert (
        InclusionVerifier.verify(
            log,
            "entry-002",
        )
        is True
    )
