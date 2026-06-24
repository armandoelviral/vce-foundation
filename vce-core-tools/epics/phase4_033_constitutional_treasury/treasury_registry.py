from epics.phase4_033_constitutional_treasury.treasury_record import (
    TreasuryRecord,
)


class TreasuryRegistry:
    def __init__(self):
        self._records = []
        self._ids = set()

    def add(self, record: TreasuryRecord):
        if record.treasury_id in self._ids:
            raise ValueError("duplicate treasury")

        self._records.append(record)
        self._ids.add(record.treasury_id)

    def records(self):
        return list(self._records)
