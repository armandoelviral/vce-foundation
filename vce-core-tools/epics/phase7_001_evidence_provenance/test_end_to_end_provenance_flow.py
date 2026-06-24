from epics.phase7_001_evidence_provenance.provenance_record import (
    ProvenanceRecord,
)
from epics.phase7_001_evidence_provenance.provenance_registry import (
    ProvenanceRegistry,
)
from epics.phase7_001_evidence_provenance.provenance_state import (
    ProvenanceState,
)
from epics.phase7_001_evidence_provenance.provenance_verifier import (
    verify_provenance,
)


def test_end_to_end_provenance_flow():
    registry = ProvenanceRegistry()

    registry.add(
        ProvenanceRecord(
            "prov.001",
            "evidence.001",
            "root",
        )
    )

    registry.add(
        ProvenanceRecord(
            "prov.002",
            "evidence.002",
            "prov.001",
        )
    )

    state = ProvenanceState.from_records(
        registry.records()
    )

    verification = verify_provenance(state)

    assert verification["verified"] is True
    assert verification["chain_depth"] == 2
