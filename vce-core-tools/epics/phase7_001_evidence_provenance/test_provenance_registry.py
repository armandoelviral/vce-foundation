from epics.phase7_001_evidence_provenance.provenance_record import (
    ProvenanceRecord,
)
from epics.phase7_001_evidence_provenance.provenance_registry import (
    ProvenanceRegistry,
)


def test_registry_adds_record():
    registry = ProvenanceRegistry()

    record = ProvenanceRecord(
        "prov.001",
        "evidence.001",
        "root",
    )

    registry.add(record)

    assert registry.records() == [record]
