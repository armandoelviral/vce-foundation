from dataclasses import dataclass

from epics.phase6_004_constitutional_trust_engine.trust_record import (
    TrustRecord,
)


@dataclass(frozen=True)
class TrustState:
    total_records: int
    total_score: int

    @classmethod
    def from_records(
        cls,
        records: list[TrustRecord],
    ):
        return cls(
            total_records=len(records),
            total_score=sum(
                record.trust_delta
                for record in records
            ),
        )
