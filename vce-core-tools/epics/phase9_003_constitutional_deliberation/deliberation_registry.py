from epics.phase9_003_constitutional_deliberation.deliberation_record import (
    DeliberationRecord,
)


class DeliberationRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: DeliberationRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
