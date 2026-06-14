from epics.epic089_replay_transparency_log.replay_transparency_entry import (
    ReplayTransparencyEntry,
)


def test_entry_contains_replay_attestation_identity():
    entry = ReplayTransparencyEntry(
        entry_id="entry-001",
        replay_id="replay-001",
        certificate_hash="hash-123",
        certificate_signature="sig-456",
        verified=True,
    )

    assert entry.entry_id == "entry-001"
    assert entry.replay_id == "replay-001"
    assert entry.certificate_hash == "hash-123"
    assert entry.certificate_signature == "sig-456"
    assert entry.verified is True


def test_entry_serializes_to_dict():
    entry = ReplayTransparencyEntry(
        entry_id="entry-001",
        replay_id="replay-001",
        certificate_hash="hash-123",
        certificate_signature="sig-456",
        verified=True,
    )

    assert entry.to_dict() == {
        "entry_id": "entry-001",
        "replay_id": "replay-001",
        "certificate_hash": "hash-123",
        "certificate_signature": "sig-456",
        "verified": True,
    }
