from dataclasses import dataclass


@dataclass(frozen=True)
class ConsensusRecord:
    consensus_id: str
    claim_id: str
    observer_id: str
    vote: bool

    def __post_init__(self):
        if not self.consensus_id:
            raise ValueError("consensus_id is required")

        if not self.claim_id:
            raise ValueError("claim_id is required")

        if not self.observer_id:
            raise ValueError("observer_id is required")
