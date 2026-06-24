from epics.phase8_005_constitutional_time_audit.time_audit_record import (
    TimeAuditRecord,
)


class TimeAuditRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: TimeAuditRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
