from epics.phase4_032_constitutional_reserves.reserve_record import (
    ReserveRecord,
)


class ReserveRegistry:
    def __init__(self):
        self._records = []
        self._reserve_ids = set()

    def add(self, record: ReserveRecord):
        if record.reserve_id in self._reserve_ids:
            raise ValueError("duplicate reserve")

        self._records.append(record)
        self._reserve_ids.add(record.reserve_id)

    def records(self):
        return list(self._records)
