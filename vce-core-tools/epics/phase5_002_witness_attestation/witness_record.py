from dataclasses import dataclass


@dataclass(frozen=True)
class WitnessRecord:
    witness_id: str
    observation_id: str
    witness_type: str

    def __post_init__(self):
        if not self.witness_id:
            raise ValueError("witness_id is required")

        if not self.observation_id:
            raise ValueError("observation_id is required")

        if not self.witness_type:
            raise ValueError("witness_type is required")
