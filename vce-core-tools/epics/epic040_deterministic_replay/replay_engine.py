from epics.epic038_replay_validator.replay_validator import (
    ReplayValidator,
)
from epics.epic041_runtime_state.runtime_state import (
    RuntimeState,
)


class ReplayEngine:

    def __init__(self):
        self.validator = ReplayValidator()

    def replay(self, events):
        if not self.validator.validate(events):
            return False

        return RuntimeState(
            event_count=len(events),
            last_sequence=events[-1]["sequence"],
        )
