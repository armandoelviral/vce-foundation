from epics.epic012_replay_runtime.replay_state import ReplayState
from epics.epic012_replay_runtime.lsn_validator import validate_lsn
from epics.epic012_replay_runtime.transition_validator import validate_transitions
from epics.epic012_replay_runtime.opcode_dispatcher import OpcodeDispatcher

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
