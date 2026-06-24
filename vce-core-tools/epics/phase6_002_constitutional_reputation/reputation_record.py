from dataclasses import dataclass


@dataclass(frozen=True)
class ReputationRecord:
    reputation_id: str
    identity_id: str
    score_delta: int

    def __post_init__(self):
        if not self.reputation_id:
            raise ValueError("reputation_id is required")

        if not self.identity_id:
            raise ValueError("identity_id is required")
