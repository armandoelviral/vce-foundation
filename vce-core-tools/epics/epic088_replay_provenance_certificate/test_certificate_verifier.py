from epics.epic088_replay_provenance_certificate.certificate_signature import (
    CertificateSignature,
)

from epics.epic088_replay_provenance_certificate.certificate_verifier import (
    CertificateVerifier,
)


def test_verifier_accepts_valid_signature():
    certificate_hash = "certificate-hash"

    signature = CertificateSignature.sign(
        certificate_hash
    )

    assert CertificateVerifier.verify(
        certificate_hash,
        signature,
    )


def test_verifier_rejects_invalid_signature():
    assert not CertificateVerifier.verify(
        "certificate-hash",
        "tampered-signature",
    )
