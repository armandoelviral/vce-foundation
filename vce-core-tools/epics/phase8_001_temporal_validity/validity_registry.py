from epics.phase8_001_temporal_validity.validity_record import (
    ValidityRecord,
)


class ValidityRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: ValidityRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
