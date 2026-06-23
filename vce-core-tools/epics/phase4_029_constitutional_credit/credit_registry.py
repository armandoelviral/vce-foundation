from epics.phase4_029_constitutional_credit.credit_record import (
    CreditRecord,
)


class CreditRegistry:
    def __init__(self):
        self._records = []
        self._credit_ids = set()

    def add(self, record: CreditRecord):
        if record.credit_id in self._credit_ids:
            raise ValueError("duplicate credit")

        self._records.append(record)
        self._credit_ids.add(record.credit_id)

    def records(self):
        return list(self._records)
