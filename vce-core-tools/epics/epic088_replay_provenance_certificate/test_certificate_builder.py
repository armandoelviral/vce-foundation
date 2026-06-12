from epics.epic088_replay_provenance_certificate.certificate_builder import (
    CertificateBuilder,
)


def test_builder_creates_certificate():
    certificate = CertificateBuilder.build(
        replay_id="replay-001",
        request_hash="request-abc",
        result_hash="result-def",
        environment_hash="env-123",
        comparator_hash="cmp-456",
    )

    assert certificate.replay_id == "replay-001"
    assert certificate.request_hash == "request-abc"
    assert certificate.result_hash == "result-def"
    assert certificate.environment_hash == "env-123"
    assert certificate.comparator_hash == "cmp-456"
