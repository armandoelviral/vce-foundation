from epics.epic088_replay_provenance_certificate.certificate_signature import (
    CertificateSignature,
)

from epics.epic088_replay_provenance_certificate.certificate_hash import (
    CertificateHash,
)

from epics.epic088_replay_provenance_certificate.replay_provenance_certificate import (
    ReplayProvenanceCertificate,
)


def test_signature_is_deterministic():
    certificate = ReplayProvenanceCertificate(
        replay_id="replay-001",
        request_hash="request-abc",
        result_hash="result-def",
        environment_hash="env-123",
        comparator_hash="cmp-456",
    )

    certificate_hash = CertificateHash.compute(certificate)

    sig1 = CertificateSignature.sign(certificate_hash)
    sig2 = CertificateSignature.sign(certificate_hash)

    assert sig1 == sig2


def test_signature_changes_when_hash_changes():
    sig1 = CertificateSignature.sign("hash-a")
    sig2 = CertificateSignature.sign("hash-b")

    assert sig1 != sig2
