from epics.phase7_001_evidence_provenance.provenance_record import (
    ProvenanceRecord,
)


class ProvenanceRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: ProvenanceRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
