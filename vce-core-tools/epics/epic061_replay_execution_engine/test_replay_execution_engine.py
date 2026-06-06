from epics.epic041_runtime_state.runtime_state import RuntimeState
from epics.epic057_runtime_opcode.runtime_opcode import RuntimeOpcode
from epics.epic061_replay_execution_engine.replay_execution_engine import (
    ReplayExecutionEngine,
)


def test_replays_multiple_opcodes_to_final_state():

    initial_state = RuntimeState(
        event_count=0,
        last_sequence=0,
    )

    opcodes = [
        RuntimeOpcode(
            name="APPEND_EVENT",
            payload={},
        ),
        RuntimeOpcode(
            name="APPEND_EVENT",
            payload={},
        ),
        RuntimeOpcode(
            name="APPEND_EVENT",
            payload={},
        ),
    ]

    engine = ReplayExecutionEngine()

    final_state = engine.replay(
        initial_state,
        opcodes,
    )

    assert final_state.event_count == 3
    assert final_state.last_sequence == 3


def test_replay_returns_false_when_opcode_fails():

    initial_state = RuntimeState(
        event_count=0,
        last_sequence=0,
    )

    opcodes = [
        RuntimeOpcode(
            name="APPEND_EVENT",
            payload={},
        ),
        RuntimeOpcode(
            name="UNKNOWN_OPCODE",
            payload={},
        ),
        RuntimeOpcode(
            name="APPEND_EVENT",
            payload={},
        ),
    ]

    engine = ReplayExecutionEngine()

    result = engine.replay(
        initial_state,
        opcodes,
    )

    assert result is False
