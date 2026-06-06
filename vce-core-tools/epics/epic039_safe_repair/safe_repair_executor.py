from epics.epic038_replay_validator.replay_validator import (
    ReplayValidator,
)


class SafeRepairExecutor:

    def __init__(self):

        self.validator = ReplayValidator()

    def execute(self, events):

        if not self.validator.validate(events):
            return False

        return True
