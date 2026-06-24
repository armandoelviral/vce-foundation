from dataclasses import dataclass


@dataclass(frozen=True)
class ReplayRecord:
    replay_id: str
    trust_id: str
    historical_epoch: int

    def __post_init__(self):
        if not self.replay_id:
            raise ValueError("replay_id is required")

        if not self.trust_id:
            raise ValueError("trust_id is required")
