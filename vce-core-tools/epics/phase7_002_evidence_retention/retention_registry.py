from epics.phase7_002_evidence_retention.retention_record import (
    RetentionRecord,
)


class RetentionRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: RetentionRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
