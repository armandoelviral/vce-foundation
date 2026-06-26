from dataclasses import dataclass

from epics.phase9_003_constitutional_deliberation.deliberation_record import (
    DeliberationRecord,
)


@dataclass(frozen=True)
class DeliberationState:
    total_deliberations: int
    total_participants: int

    @classmethod
    def from_records(
        cls,
        records: list[DeliberationRecord],
    ):
        return cls(
            total_deliberations=len(records),
            total_participants=sum(
                record.participants
                for record in records
            ),
        )
