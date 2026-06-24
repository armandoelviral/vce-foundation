from dataclasses import dataclass

from epics.phase7_001_evidence_provenance.provenance_record import (
    ProvenanceRecord,
)


@dataclass(frozen=True)
class ProvenanceState:
    total_records: int
    chain_depth: int

    @classmethod
    def from_records(
        cls,
        records: list[ProvenanceRecord],
    ):
        return cls(
            total_records=len(records),
            chain_depth=len(records),
        )
