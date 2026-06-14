from epics.epic089_replay_transparency_log.replay_transparency_entry import (
    ReplayTransparencyEntry,
)

from epics.epic089_replay_transparency_log.replay_transparency_log import (
    ReplayTransparencyLog,
)

from epics.epic089_replay_transparency_log.replay_inclusion_proof import (
    ReplayInclusionProof,
)


def test_inclusion_proof_finds_replay():

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

    proof = ReplayInclusionProof.build(
        log.records,
        "replay-001",
    )

    assert proof["included"] is True
    assert proof["sequence"] == 1


def test_inclusion_proof_rejects_missing_replay():

    log = ReplayTransparencyLog()

    proof = ReplayInclusionProof.build(
        log.records,
        "missing-replay",
    )

    assert proof["included"] is False
