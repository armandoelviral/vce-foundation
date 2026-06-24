from epics.phase6_004_constitutional_trust_engine.trust_record import (
    TrustRecord,
)


class TrustRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: TrustRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
