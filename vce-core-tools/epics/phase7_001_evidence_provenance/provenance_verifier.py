from epics.phase7_001_evidence_provenance.provenance_state import (
    ProvenanceState,
)


def verify_provenance(
    state: ProvenanceState,
):
    return {
        "verified": state.chain_depth > 0,
        "chain_depth": state.chain_depth,
        "total_records": state.total_records,
    }
