from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)

from phase3.certificate_transparency.transparency_log import (
    TransparencyLog,
)

from phase3.certificate_transparency.transparency_submission import (
    TransparencySubmission,
)


def test_submission_creates_entry():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    log = TransparencyLog()

    entry = TransparencySubmission.submit(
        entry_id="entry-001",
        certificate=certificate,
        log=log,
    )

    assert entry.entry_id == "entry-001"


def test_submission_preserves_certificate_id():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    log = TransparencyLog()

    entry = TransparencySubmission.submit(
        entry_id="entry-001",
        certificate=certificate,
        log=log,
    )

    assert (
        entry.certificate_id
        == "cert-001"
    )


def test_submission_adds_to_log():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    log = TransparencyLog()

    TransparencySubmission.submit(
        entry_id="entry-001",
        certificate=certificate,
        log=log,
    )

    assert log.count() == 1
