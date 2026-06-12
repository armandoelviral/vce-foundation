from epics.epic088_replay_provenance_certificate.certificate_hash import (
    CertificateHash,
)

from epics.epic088_replay_provenance_certificate.replay_provenance_certificate import (
    ReplayProvenanceCertificate,
)


def test_hash_is_deterministic():
    certificate = ReplayProvenanceCertificate(
        replay_id="replay-001",
        request_hash="request-abc",
        result_hash="result-def",
        environment_hash="env-123",
        comparator_hash="cmp-456",
    )

    hash1 = CertificateHash.compute(certificate)
    hash2 = CertificateHash.compute(certificate)

    assert hash1 == hash2


def test_hash_changes_when_certificate_changes():
    certificate_a = ReplayProvenanceCertificate(
        replay_id="replay-001",
        request_hash="request-abc",
        result_hash="result-def",
        environment_hash="env-123",
        comparator_hash="cmp-456",
    )

    certificate_b = ReplayProvenanceCertificate(
        replay_id="replay-002",
        request_hash="request-abc",
        result_hash="result-def",
        environment_hash="env-123",
        comparator_hash="cmp-456",
    )

    assert (
        CertificateHash.compute(certificate_a)
        != CertificateHash.compute(certificate_b)
    )
