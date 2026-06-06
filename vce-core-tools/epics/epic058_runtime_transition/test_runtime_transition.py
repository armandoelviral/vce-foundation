from epics.epic041_runtime_state.runtime_state import (
    RuntimeState,
)

from epics.epic057_runtime_opcode.runtime_opcode import (
    RuntimeOpcode,
)

from epics.epic058_runtime_transition.runtime_transition import (
    RuntimeTransition,
)


def test_transition_updates_runtime_state():

    state = RuntimeState(
        event_count=1,
        last_sequence=1,
    )

    opcode = RuntimeOpcode(
        name="APPEND_EVENT",
        payload={},
    )

    transition = RuntimeTransition()

    new_state = transition.apply(
        state,
        opcode,
    )

    assert new_state.event_count == 2
    assert new_state.last_sequence == 2
