from epics.phase5_008_constitutional_reality_ledger.reality_ledger_record import (
    RealityLedgerRecord,
)


class RealityLedgerRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: RealityLedgerRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
