from epics.phase4_030_constitutional_risk.risk_record import (
    RiskRecord,
)


class RiskRegistry:
    def __init__(self):
        self._records = []
        self._risk_ids = set()

    def add(self, record: RiskRecord):
        if record.risk_id in self._risk_ids:
            raise ValueError("duplicate risk")

        self._records.append(record)
        self._risk_ids.add(record.risk_id)

    def records(self):
        return list(self._records)
