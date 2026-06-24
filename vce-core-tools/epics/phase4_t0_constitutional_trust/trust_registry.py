from epics.phase4_t0_constitutional_trust.trust_record import (
    TrustRecord,
)


class TrustRegistry:
    def __init__(self):
        self._records = []
        self._trust_ids = set()

    def add(self, record: TrustRecord):
        if record.trust_id in self._trust_ids:
            raise ValueError("duplicate trust")

        self._records.append(record)
        self._trust_ids.add(record.trust_id)

    def records(self):
        return list(self._records)
