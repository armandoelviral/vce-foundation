from epics.epic060_runtime_execution_engine.runtime_execution_engine import (
    RuntimeExecutionEngine,
)


class ReplayExecutionEngine:

    def __init__(self):
        self.engine = RuntimeExecutionEngine()

    def replay(
        self,
        initial_state,
        opcodes,
    ):
        state = initial_state

        for opcode in opcodes:
            state = self.engine.execute(
                state,
                opcode,
            )

            if state is False:
                return False

        return state
