from epics.phase7_001_evidence_provenance.provenance_state import (
    ProvenanceState,
)
from epics.phase7_001_evidence_provenance.provenance_verifier import (
    verify_provenance,
)


def test_provenance_verified():
    state = ProvenanceState(
        total_records=2,
        chain_depth=2,
    )

    result = verify_provenance(state)

    assert result["verified"] is True


def test_empty_provenance_not_verified():
    state = ProvenanceState(
        total_records=0,
        chain_depth=0,
    )

    result = verify_provenance(state)

    assert result["verified"] is False
