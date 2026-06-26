from epics.phase9_007_constitutional_outcome.outcome_record import (
    OutcomeRecord,
)


class OutcomeRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: OutcomeRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
