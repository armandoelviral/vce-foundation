from epics.phase9_004_constitutional_decision.decision_record import (
    DecisionRecord,
)


class DecisionRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: DecisionRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
