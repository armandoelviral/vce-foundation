from epics.epic012_replay_runtime.opcode_dispatcher import (
    OpcodeDispatcher,
)
from epics.epic012_replay_runtime.replay_state import (
    ReplayState,
)


def test_opcode_dispatcher_processes_events():

    state = ReplayState()
    dispatcher = OpcodeDispatcher()

    events = [
        {
            "lsn": 1,
            "opcode": "APPEND_EVIDENCE",
            "payload": "artifact-001",
        },
        {
            "lsn": 2,
            "opcode": "REGISTER_ARTIFACT",
            "payload": "artifact-001",
        },
        {
            "lsn": 3,
            "opcode": "SEAL_SNAPSHOT",
            "payload": "snapshot-001",
        },
    ]

    for event in events:
        state = dispatcher.dispatch(
            state,
            event,
        )

    assert state.sequence_number == 3
    assert len(state.events) == 3


def test_opcode_dispatcher_updates_state_hash():

    state = ReplayState()
    dispatcher = OpcodeDispatcher()

    event = {
        "lsn": 1,
        "opcode": "APPEND_EVIDENCE",
        "payload": "artifact-001",
    }

    state = dispatcher.dispatch(
        state,
        event,
    )

    assert state.state_hash is not None
    assert len(state.state_hash) > 0
