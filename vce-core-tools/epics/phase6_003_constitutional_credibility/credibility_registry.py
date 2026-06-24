from epics.phase6_003_constitutional_credibility.credibility_record import (
    CredibilityRecord,
)


class CredibilityRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: CredibilityRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
