from epics.phase5_006_reality_verification.reality_claim import (
    RealityClaim,
)


class RealityRegistry:
    def __init__(self):
        self._records = []
        self._ids = set()

    def add(self, record: RealityClaim):
        if record.claim_id in self._ids:
            raise ValueError("duplicate claim")

        self._records.append(record)
        self._ids.add(record.claim_id)

    def records(self):
        return list(self._records)
