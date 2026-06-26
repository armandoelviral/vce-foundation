from dataclasses import dataclass

from epics.phase9_004_constitutional_decision.decision_record import (
    DecisionRecord,
)


@dataclass(frozen=True)
class DecisionState:
    total_decisions: int
    accepted: int
    rejected: int

    @classmethod
    def from_records(
        cls,
        records: list[DecisionRecord],
    ):
        accepted = sum(
            1
            for record in records
            if record.outcome == "accepted"
        )

        rejected = sum(
            1
            for record in records
            if record.outcome == "rejected"
        )

        return cls(
            total_decisions=len(records),
            accepted=accepted,
            rejected=rejected,
        )
