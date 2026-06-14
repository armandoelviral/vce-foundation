from epics.epic089_replay_transparency_log.replay_transparency_entry import (
    ReplayTransparencyEntry,
)

from epics.epic089_replay_transparency_log.replay_transparency_log import (
    ReplayTransparencyLog,
)

from epics.epic089_replay_transparency_log.replay_log_verifier import (
    ReplayLogVerifier,
)


def test_verifier_accepts_valid_log():

    log = ReplayTransparencyLog()

    log.append(
        ReplayTransparencyEntry(
            entry_id="entry-001",
            replay_id="replay-001",
            certificate_hash="hash-001",
            certificate_signature="sig-001",
            verified=True,
        )
    )

    log.append(
        ReplayTransparencyEntry(
            entry_id="entry-002",
            replay_id="replay-002",
            certificate_hash="hash-002",
            certificate_signature="sig-002",
            verified=True,
        )
    )

    assert ReplayLogVerifier.verify(log.records)


def test_verifier_detects_tampering():

    log = ReplayTransparencyLog()

    log.append(
        ReplayTransparencyEntry(
            entry_id="entry-001",
            replay_id="replay-001",
            certificate_hash="hash-001",
            certificate_signature="sig-001",
            verified=True,
        )
    )

    log.append(
        ReplayTransparencyEntry(
            entry_id="entry-002",
            replay_id="replay-002",
            certificate_hash="hash-002",
            certificate_signature="sig-002",
            verified=True,
        )
    )

    log.records[1] = type(log.records[1])(
        sequence=2,
        previous_hash="tampered",
        current_hash=log.records[1].current_hash,
        replay_id=log.records[1].replay_id,
    )

    assert not ReplayLogVerifier.verify(log.records)
