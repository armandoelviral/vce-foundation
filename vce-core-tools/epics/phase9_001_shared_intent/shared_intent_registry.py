from epics.phase9_001_shared_intent.shared_intent_record import (
    SharedIntentRecord,
)


class SharedIntentRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: SharedIntentRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
