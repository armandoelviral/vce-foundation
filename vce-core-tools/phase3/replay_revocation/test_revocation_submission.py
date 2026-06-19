from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)

from phase3.replay_revocation.revocation_registry import (
    RevocationRegistry,
)

from phase3.replay_revocation.revocation_submission import (
    RevocationSubmission,
)


def test_submission_creates_revocation():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    registry = RevocationRegistry()

    revocation = (
        RevocationSubmission.submit(
            revocation_id="rev-001",
            certificate=certificate,
            reason="key_compromise",
            registry=registry,
        )
    )

    assert (
        revocation.revocation_id
        == "rev-001"
    )


def test_submission_preserves_certificate_id():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    registry = RevocationRegistry()

    revocation = (
        RevocationSubmission.submit(
            revocation_id="rev-001",
            certificate=certificate,
            reason="key_compromise",
            registry=registry,
        )
    )

    assert (
        revocation.certificate_id
        == "cert-001"
    )


def test_submission_adds_to_registry():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    registry = RevocationRegistry()

    RevocationSubmission.submit(
        revocation_id="rev-001",
        certificate=certificate,
        reason="key_compromise",
        registry=registry,
    )

    assert registry.count() == 1
