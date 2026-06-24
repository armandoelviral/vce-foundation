from dataclasses import dataclass

from epics.phase5_001_verifiable_observation.observation_record import (
    ObservationRecord,
)


@dataclass(frozen=True)
class ObservationState:
    total_observations: int

    @classmethod
    def from_records(
        cls,
        records: list[ObservationRecord],
    ):
        return cls(
            total_observations=len(records)
        )
