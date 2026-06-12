from epics.epic088_replay_provenance_certificate.replay_provenance_attestation import (
    ReplayProvenanceAttestation,
)


def test_attestation_contains_all_evidence():
    attestation = ReplayProvenanceAttestation(
        replay_id="replay-001",
        certificate_hash="hash-123",
        certificate_signature="sig-456",
        verified=True,
    )

    assert attestation.replay_id == "replay-001"
    assert attestation.certificate_hash == "hash-123"
    assert attestation.certificate_signature == "sig-456"
    assert attestation.verified is True


def test_attestation_serializes():
    attestation = ReplayProvenanceAttestation(
        replay_id="replay-001",
        certificate_hash="hash-123",
        certificate_signature="sig-456",
        verified=True,
    )

    assert attestation.to_dict() == {
        "replay_id": "replay-001",
        "certificate_hash": "hash-123",
        "certificate_signature": "sig-456",
        "verified": True,
    }
