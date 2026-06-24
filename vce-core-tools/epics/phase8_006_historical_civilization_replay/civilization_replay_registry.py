from epics.phase8_006_historical_civilization_replay.civilization_replay_record import (
    CivilizationReplayRecord,
)


class CivilizationReplayRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: CivilizationReplayRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
