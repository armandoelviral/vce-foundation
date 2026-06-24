from epics.phase8_003_historical_trust_replay.replay_record import (
    ReplayRecord,
)


class ReplayRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: ReplayRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
