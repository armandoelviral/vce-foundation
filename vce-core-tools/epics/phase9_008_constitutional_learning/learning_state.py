from dataclasses import dataclass

from epics.phase9_008_constitutional_learning.learning_record import (
    LearningRecord,
)


@dataclass(frozen=True)
class LearningState:
    total_learning: int

    @classmethod
    def from_records(
        cls,
        records: list[LearningRecord],
    ):
        return cls(
            total_learning=len(records),
        )
