from dataclasses import dataclass

from epics.phase6_002_constitutional_reputation.reputation_record import (
    ReputationRecord,
)


@dataclass(frozen=True)
class ReputationState:
    total_records: int
    total_score: int

    @classmethod
    def from_records(
        cls,
        records: list[ReputationRecord],
    ):
        return cls(
            total_records=len(records),
            total_score=sum(
                record.score_delta
                for record in records
            ),
        )
