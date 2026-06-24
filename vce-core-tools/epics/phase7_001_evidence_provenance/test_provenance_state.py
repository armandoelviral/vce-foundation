from epics.phase7_001_evidence_provenance.provenance_record import (
    ProvenanceRecord,
)
from epics.phase7_001_evidence_provenance.provenance_state import (
    ProvenanceState,
)


def test_builds_provenance_state():
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

    state = ProvenanceState.from_records(records)

    assert state.total_records == 2
    assert state.chain_depth == 2


def test_empty_provenance_state():
    state = ProvenanceState.from_records([])

    assert state.total_records == 0
    assert state.chain_depth == 0
