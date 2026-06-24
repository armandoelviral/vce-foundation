from epics.phase8_002_trust_expiration.expiration_record import (
    ExpirationRecord,
)


class ExpirationRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: ExpirationRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
