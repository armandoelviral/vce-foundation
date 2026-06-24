from dataclasses import dataclass

from epics.phase6_005_constitutional_trust_score.trust_score_record import (
    TrustScoreRecord,
)


@dataclass(frozen=True)
class TrustScoreState:
    total_records: int
    average_score: int

    @classmethod
    def from_records(
        cls,
        records: list[TrustScoreRecord],
    ):
        if not records:
            return cls(
                total_records=0,
                average_score=0,
            )

        average = int(
            sum(record.score for record in records)
            / len(records)
        )

        return cls(
            total_records=len(records),
            average_score=average,
        )
