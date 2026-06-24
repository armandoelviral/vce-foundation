from epics.phase6_002_constitutional_reputation.reputation_record import (
    ReputationRecord,
)


class ReputationRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: ReputationRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
