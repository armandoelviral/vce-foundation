from epics.phase7_001_evidence_provenance.provenance_record import (
    ProvenanceRecord,
)


def build_provenance_chain(
    records: list[ProvenanceRecord],
):
    return {
        "length": len(records),
    }
