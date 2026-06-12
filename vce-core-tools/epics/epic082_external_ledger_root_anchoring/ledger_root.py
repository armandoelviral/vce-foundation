from dataclasses import dataclass


@dataclass(frozen=True)
class LedgerRoot:
    root_hash: str
    sequence_start: int
    sequence_end: int
    evidence_count: int
    region: str
    generated_at: str

    def to_dict(self):

        return {
            "root_hash": self.root_hash,
            "sequence_start": self.sequence_start,
            "sequence_end": self.sequence_end,
            "evidence_count": self.evidence_count,
            "region": self.region,
            "generated_at": self.generated_at,
        }
