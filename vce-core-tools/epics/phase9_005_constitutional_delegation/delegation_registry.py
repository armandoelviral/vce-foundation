from epics.phase9_005_constitutional_delegation.delegation_record import (
    DelegationRecord,
)


class DelegationRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: DelegationRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
