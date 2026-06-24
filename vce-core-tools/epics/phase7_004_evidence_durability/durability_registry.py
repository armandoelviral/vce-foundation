from epics.phase7_004_evidence_durability.durability_record import (
    DurabilityRecord,
)


class DurabilityRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: DurabilityRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
