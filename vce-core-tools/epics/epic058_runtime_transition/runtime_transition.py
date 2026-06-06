from epics.epic041_runtime_state.runtime_state import (
    RuntimeState,
)


class RuntimeTransition:

    def apply(
        self,
        state,
        opcode,
    ):

        if opcode.name == "APPEND_EVENT":

            return RuntimeState(
                event_count=(
                    state.event_count + 1
                ),
                last_sequence=(
                    state.last_sequence + 1
                ),
            )

        return state
