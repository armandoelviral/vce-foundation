from epics.phase7_001_evidence_provenance.provenance_record import (
    ProvenanceRecord,
)
from epics.phase7_001_evidence_provenance.provenance_chain import (
    build_provenance_chain,
)


def test_builds_chain():
    records = [
        ProvenanceRecord(
            "prov.001",
            "evidence.001",
            "root",
        ),
        ProvenanceRecord(
            "prov.002",
            "evidence.002",
            "prov.001",
        ),
    ]

    chain = build_provenance_chain(records)

    assert chain["length"] == 2
