from dataclasses import dataclass


@dataclass(frozen=True)
class RealityClaim:
    claim_id: str
    observation_id: str
    claim_value: str

    def __post_init__(self):
        if not self.claim_id:
            raise ValueError("claim_id is required")

        if not self.observation_id:
            raise ValueError("observation_id is required")

        if not self.claim_value:
            raise ValueError("claim_value is required")
