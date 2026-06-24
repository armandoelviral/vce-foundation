from dataclasses import dataclass

from epics.phase6_003_constitutional_credibility.credibility_record import (
    CredibilityRecord,
)


@dataclass(frozen=True)
class CredibilityState:
    total_records: int
    total_score: int

    @classmethod
    def from_records(
        cls,
        records: list[CredibilityRecord],
    ):
        return cls(
            total_records=len(records),
            total_score=sum(
                record.credibility_delta for record in records
            ),
        )
