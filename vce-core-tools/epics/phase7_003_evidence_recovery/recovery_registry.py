from epics.phase7_003_evidence_recovery.recovery_record import (
    RecoveryRecord,
)


class RecoveryRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: RecoveryRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
