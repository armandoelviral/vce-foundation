from epics.phase6_001_constitutional_identity.identity_record import (
    IdentityRecord,
)


class IdentityRegistry:
    def __init__(self):
        self._records = []
        self._ids = set()

    def add(self, record: IdentityRecord):
        if record.identity_id in self._ids:
            raise ValueError("duplicate identity")

        self._records.append(record)
        self._ids.add(record.identity_id)

    def records(self):
        return list(self._records)
