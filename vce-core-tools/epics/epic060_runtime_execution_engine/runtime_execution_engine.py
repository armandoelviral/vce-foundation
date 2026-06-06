from epics.epic058_runtime_transition.runtime_transition import (
    RuntimeTransition,
)

from epics.epic059_transition_validator.transition_validator import (
    TransitionValidator,
)


class RuntimeExecutionEngine:

    def __init__(self):

        self.transition = (
            RuntimeTransition()
        )

        self.validator = (
            TransitionValidator()
        )

    def execute(
        self,
        state,
        opcode,
    ):

        if opcode.name != "APPEND_EVENT":
            return False

        new_state = (
            self.transition.apply(
                state,
                opcode,
            )
        )

        valid = (
            self.validator.validate(
                state,
                new_state,
                opcode,
            )
        )

        if not valid:
            return False

        return new_state
