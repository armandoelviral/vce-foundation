from epics.epic012_replay_runtime.lsn_validator import validate_lsn
from epics.epic012_replay_runtime.replay_engine import ReplayEngine
from epics.epic012_replay_runtime.transition_validator import (
    validate_transitions,
)
from epics.epic012_replay_runtime.wal_reader import read_wal


def test_wal_events_are_valid():

    path = "epics/epic012_replay_runtime/governance.wal"

    events = read_wal(path)

    assert validate_lsn(events) is True
    assert validate_transitions(events) is True


def test_wal_replays_to_state_hash():

    path = "epics/epic012_replay_runtime/governance.wal"

    events = read_wal(path)

    engine = ReplayEngine()

    state = engine.replay(
        [
            f"{event['lsn']}|{event['opcode']}|{event['payload']}"
            for event in events
        ]
    )

    assert isinstance(state.state_hash, str)
    assert len(state.state_hash) == 64
