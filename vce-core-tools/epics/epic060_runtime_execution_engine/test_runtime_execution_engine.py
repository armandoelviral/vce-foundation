from epics.epic041_runtime_state.runtime_state import (
    RuntimeState,
)

from epics.epic057_runtime_opcode.runtime_opcode import (
    RuntimeOpcode,
)

from epics.epic060_runtime_execution_engine.runtime_execution_engine import (
    RuntimeExecutionEngine,
)


def test_executes_valid_transition():

    state = RuntimeState(
        event_count=1,
        last_sequence=1,
    )

    opcode = RuntimeOpcode(
        name="APPEND_EVENT",
        payload={},
    )

    engine = RuntimeExecutionEngine()

    new_state = engine.execute(
        state,
        opcode,
    )

    assert new_state.event_count == 2
    assert new_state.last_sequence == 2


def test_rejects_invalid_transition():

    state = RuntimeState(
        event_count=1,
        last_sequence=1,
    )

    opcode = RuntimeOpcode(
        name="UNKNOWN_OPCODE",
        payload={},
    )

    engine = RuntimeExecutionEngine()

    result = engine.execute(
        state,
        opcode,
    )

    assert result is False
