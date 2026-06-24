from epics.phase5_003_physical_evidence.evidence_record import (
    EvidenceRecord,
)


class EvidenceRegistry:
    def __init__(self):
        self._records = []
        self._ids = set()

    def add(self, record: EvidenceRecord):
        if record.evidence_id in self._ids:
            raise ValueError("duplicate evidence")

        self._records.append(record)
        self._ids.add(record.evidence_id)

    def records(self):
        return list(self._records)
