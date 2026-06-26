from dataclasses import dataclass

from epics.phase9_001_shared_intent.shared_intent_record import (
    SharedIntentRecord,
)


@dataclass(frozen=True)
class SharedIntentState:
    total_intents: int
    total_participants: int

    @classmethod
    def from_records(
        cls,
        records: list[SharedIntentRecord],
    ):
        return cls(
            total_intents=len(records),
            total_participants=sum(
                record.participants
                for record in records
            ),
        )
