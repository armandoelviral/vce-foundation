from epics.epic089_replay_transparency_log.replay_transparency_entry import (
    ReplayTransparencyEntry,
)

from epics.epic089_replay_transparency_log.replay_transparency_log import (
    ReplayTransparencyLog,
)

from epics.epic089_replay_transparency_log.replay_log_verifier import (
    ReplayLogVerifier,
)

from epics.epic089_replay_transparency_log.replay_inclusion_proof import (
    ReplayInclusionProof,
)


def test_end_to_end_replay_transparency_flow():

    log = ReplayTransparencyLog()

    entry = ReplayTransparencyEntry(
        entry_id="entry-001",
        replay_id="replay-001",
        certificate_hash="hash-001",
        certificate_signature="sig-001",
        verified=True,
    )

    log.append(entry)

    assert ReplayLogVerifier.verify(
        log.records
    )

    proof = ReplayInclusionProof.build(
        log.records,
        "replay-001",
    )

    assert proof["included"] is True
