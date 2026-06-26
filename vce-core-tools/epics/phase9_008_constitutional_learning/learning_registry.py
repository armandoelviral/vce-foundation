from epics.phase9_008_constitutional_learning.learning_record import (
    LearningRecord,
)


class LearningRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: LearningRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
