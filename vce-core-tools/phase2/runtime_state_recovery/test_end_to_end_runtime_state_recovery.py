from phase2.runtime_state_recovery.runtime_state_model import (
    RuntimeState,
)

from phase2.runtime_state_recovery.replay_state_rebuilder import (
    ReplayStateRebuilder,
)

from phase2.runtime_state_recovery.snapshot_restore_model import (
    SnapshotRestoreModel,
)

from phase2.runtime_state_recovery.incremental_replay_from_snapshot import (
    IncrementalReplayFromSnapshot,
)

from phase2.runtime_state_recovery.state_hash_verifier import (
    StateHashVerifier,
)

from phase2.runtime_state_recovery.recovery_report import (
    RecoveryReport,
)


def test_end_to_end_runtime_state_recovery():

    full_rebuilder = ReplayStateRebuilder()

    full_state = full_rebuilder.rebuild(
        events=[
            {
                "lsn": 1,
                "opcode": "EVENT_A",
            },
            {
                "lsn": 2,
                "opcode": "EVENT_B",
            },
        ],
    )

    assert full_state.events_applied == 2
    assert full_state.last_lsn == 2

    snapshot = SnapshotRestoreModel(
        lsn=2,
        events_applied=2,
        state_hash=full_state.state_hash,
    )

    restored_state = snapshot.restore()

    assert isinstance(
        restored_state,
        RuntimeState,
    )

    incremental = IncrementalReplayFromSnapshot()

    recovered_state = incremental.rebuild(
        snapshot_state=restored_state,
        events=[
            {
                "lsn": 3,
                "opcode": "EVENT_C",
            },
        ],
    )

    assert recovered_state.events_applied == 3
    assert recovered_state.last_lsn == 3

    verifier = StateHashVerifier()

    hash_valid = verifier.verify(
        state=recovered_state,
        expected_hash=recovered_state.state_hash,
    )

    assert hash_valid is True

    report = RecoveryReport(
        recovery_id="recovery-001",
        recovered=True,
        state_hash_valid=hash_valid,
    )

    assert report.recovered is True
    assert report.state_hash_valid is True
