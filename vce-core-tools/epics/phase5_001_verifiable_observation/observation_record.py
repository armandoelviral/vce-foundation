from dataclasses import dataclass


@dataclass(frozen=True)
class ObservationRecord:
    observation_id: str
    observer_id: str
    observation_type: str
    observation_value: str

    def __post_init__(self):
        if not self.observation_id:
            raise ValueError("observation_id is required")

        if not self.observer_id:
            raise ValueError("observer_id is required")

        if not self.observation_type:
            raise ValueError("observation_type is required")

        if not self.observation_value:
            raise ValueError("observation_value is required")
