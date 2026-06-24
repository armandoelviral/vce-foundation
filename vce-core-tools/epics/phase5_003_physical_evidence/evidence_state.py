from dataclasses import dataclass

from epics.phase5_003_physical_evidence.evidence_record import (
    EvidenceRecord,
)


@dataclass(frozen=True)
class EvidenceState:
    total_evidence: int

    @classmethod
    def from_records(
        cls,
        records: list[EvidenceRecord],
    ):
        return cls(
            total_evidence=len(records)
        )
