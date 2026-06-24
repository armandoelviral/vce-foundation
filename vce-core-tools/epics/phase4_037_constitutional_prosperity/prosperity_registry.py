from epics.phase4_037_constitutional_prosperity.prosperity_record import (
    ProsperityRecord,
)


class ProsperityRegistry:
    def __init__(self):
        self._records = []
        self._ids = set()

    def add(self, record: ProsperityRecord):
        if record.prosperity_id in self._ids:
            raise ValueError("duplicate prosperity")

        self._records.append(record)
        self._ids.add(record.prosperity_id)

    def records(self):
        return list(self._records)
