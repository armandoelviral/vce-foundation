from epics.epic089_replay_transparency_log.replay_transparency_entry import (
    ReplayTransparencyEntry,
)

from epics.epic089_replay_transparency_log.replay_transparency_log import (
    ReplayTransparencyLog,
)


def test_log_hash_chain_links_records():
    log = ReplayTransparencyLog()

    entry_1 = ReplayTransparencyEntry(
        entry_id="entry-001",
        replay_id="replay-001",
        certificate_hash="hash-123",
        certificate_signature="sig-456",
        verified=True,
    )

    entry_2 = ReplayTransparencyEntry(
        entry_id="entry-002",
        replay_id="replay-002",
        certificate_hash="hash-789",
        certificate_signature="sig-999",
        verified=True,
    )

    record_1 = log.append(entry_1)
    record_2 = log.append(entry_2)

    assert record_2.previous_hash == record_1.current_hash


def test_log_exposes_records():
    log = ReplayTransparencyLog()

    entry = ReplayTransparencyEntry(
        entry_id="entry-001",
        replay_id="replay-001",
        certificate_hash="hash-123",
        certificate_signature="sig-456",
        verified=True,
    )

    log.append(entry)

    assert len(log.records) == 1
    assert log.records[0].replay_id == "replay-001"
