from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)

from phase3.replay_certification_engine.certificate_verifier import (
    CertificateVerifier,
)


def test_valid_certificate_passes():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    assert (
        CertificateVerifier.verify(
            certificate
        )
        is True
    )


def test_missing_certificate_id_fails():

    certificate = ReplayCertificateRecord(
        certificate_id="",
        replay_id="replay-001",
        status="PASS",
    )

    assert (
        CertificateVerifier.verify(
            certificate
        )
        is False
    )


def test_missing_replay_id_fails():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="",
        status="PASS",
    )

    assert (
        CertificateVerifier.verify(
            certificate
        )
        is False
    )


def test_missing_status_fails():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="",
    )

    assert (
        CertificateVerifier.verify(
            certificate
        )
        is False
    )
