from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)

from phase3.replay_certification_engine.certificate_attestation import (
    CertificateAttestation,
)


def test_attestation_subject():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    attestation = (
        CertificateAttestation.attest(
            attestation_id="att-001",
            certificate=certificate,
        )
    )

    assert attestation.subject == "replay_certificate"


def test_attestation_uses_certificate_id():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    attestation = (
        CertificateAttestation.attest(
            attestation_id="att-001",
            certificate=certificate,
        )
    )

    assert (
        attestation.evidence_hash
        == "cert-001"
    )


def test_attestation_preserves_attestation_id():

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    attestation = (
        CertificateAttestation.attest(
            attestation_id="att-001",
            certificate=certificate,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
