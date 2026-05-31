from replay_state import ReplayState
from lsn_validator import validate_lsn
from transition_validator import validate_transitions
from opcode_dispatcher import OpcodeDispatcher


class RuntimeCore:

    def __init__(self):
        self.dispatcher = OpcodeDispatcher()

    def execute(self, events):

        if not validate_lsn(events):
            raise ValueError("INVALID_LSN_SEQUENCE")

        if not validate_transitions(events):
            raise ValueError("INVALID_TRANSITION_SEQUENCE")

        state = ReplayState()

        for event in events:
            state = self.dispatcher.dispatch(
                state,
                event
            )

        return state
