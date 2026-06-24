from epics.phase4_036_constitutional_sustainability.sustainability_record import (
    SustainabilityRecord,
)


class SustainabilityRegistry:
    def __init__(self):
        self._records = []
        self._ids = set()

    def add(self, record: SustainabilityRecord):
        if record.sustainability_id in self._ids:
            raise ValueError(
                "duplicate sustainability"
            )

        self._records.append(record)
        self._ids.add(record.sustainability_id)

    def records(self):
        return list(self._records)
