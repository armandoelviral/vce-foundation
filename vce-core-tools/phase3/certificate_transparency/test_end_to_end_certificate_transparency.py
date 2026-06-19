from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)

from phase3.certificate_transparency.transparency_log import (
    TransparencyLog,
)

from phase3.certificate_transparency.transparency_submission import (
    TransparencySubmission,
)

from phase3.certificate_transparency.inclusion_verifier import (
    InclusionVerifier,
)

from phase3.certificate_transparency.transparency_query import (
    TransparencyQuery,
)

from phase3.certificate_transparency.transparency_report import (
    TransparencyReport,
)

from phase3.certificate_transparency.transparency_attestation import (
    TransparencyAttestation,
)


def test_end_to_end_certificate_transparency():

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
        InclusionVerifier.verify(
            log,
            "entry-001",
        )
        is True
    )

    query = TransparencyQuery(
        log
    )

    recovered = query.by_id(
        "entry-001"
    )

    assert recovered == entry

    report = TransparencyReport(
        log
    )

    assert (
        report.entry_count()
        == 1
    )

    assert (
        report.entry_ids()
        == ["entry-001"]
    )

    attestation = (
        TransparencyAttestation.attest(
            attestation_id="att-001",
            entry=entry,
        )
    )

    assert (
        attestation.subject
        == "transparency_entry"
    )

    assert (
        attestation.evidence_hash
        == "entry-001"
    )
