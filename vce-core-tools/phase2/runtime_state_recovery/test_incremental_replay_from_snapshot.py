from phase2.runtime_state_recovery.runtime_state_model import (
    RuntimeState,
)

from phase2.runtime_state_recovery.incremental_replay_from_snapshot import (
    IncrementalReplayFromSnapshot,
)


def test_incremental_replay_starts_from_snapshot_state():

    snapshot_state = RuntimeState(
        events_applied=10,
        last_lsn=10,
        state_hash="snapshot-hash",
    )

    replay = IncrementalReplayFromSnapshot()

    recovered = replay.rebuild(
        snapshot_state=snapshot_state,
        events=[],
    )

    assert recovered.events_applied == 10
    assert recovered.last_lsn == 10
    assert recovered.state_hash == "snapshot-hash"


def test_incremental_replay_applies_remaining_events():

    snapshot_state = RuntimeState(
        events_applied=10,
        last_lsn=10,
        state_hash="snapshot-hash",
    )

    replay = IncrementalReplayFromSnapshot()

    recovered = replay.rebuild(
        snapshot_state=snapshot_state,
        events=[
            {
                "lsn": 11,
                "opcode": "EVENT_A",
            },
            {
                "lsn": 12,
                "opcode": "EVENT_B",
            },
        ],
    )

    assert recovered.events_applied == 12
    assert recovered.last_lsn == 12


def test_incremental_replay_changes_hash_after_events():

    snapshot_state = RuntimeState(
        events_applied=10,
        last_lsn=10,
        state_hash="snapshot-hash",
    )

    replay = IncrementalReplayFromSnapshot()

    recovered = replay.rebuild(
        snapshot_state=snapshot_state,
        events=[
            {
                "lsn": 11,
                "opcode": "EVENT_A",
            },
        ],
    )

    assert recovered.state_hash != "snapshot-hash"
