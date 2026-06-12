from epics.epic088_replay_provenance_certificate.replay_provenance_certificate import (
    ReplayProvenanceCertificate,
)


def test_certificate_contains_replay_identity():
    certificate = ReplayProvenanceCertificate(
        replay_id="replay-001",
        request_hash="request-abc123",
        result_hash="result-def456",
        environment_hash="environment-789",
        comparator_hash="comparator-xyz",
    )

    assert certificate.replay_id == "replay-001"
    assert certificate.request_hash == "request-abc123"
    assert certificate.result_hash == "result-def456"
    assert certificate.environment_hash == "environment-789"
    assert certificate.comparator_hash == "comparator-xyz"


def test_certificate_serializes_to_dict():
    certificate = ReplayProvenanceCertificate(
        replay_id="replay-001",
        request_hash="request-abc123",
        result_hash="result-def456",
        environment_hash="environment-789",
        comparator_hash="comparator-xyz",
    )

    assert certificate.to_dict() == {
        "replay_id": "replay-001",
        "request_hash": "request-abc123",
        "result_hash": "result-def456",
        "environment_hash": "environment-789",
        "comparator_hash": "comparator-xyz",
    }
