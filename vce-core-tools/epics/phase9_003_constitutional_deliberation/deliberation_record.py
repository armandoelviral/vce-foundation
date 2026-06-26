from dataclasses import dataclass


@dataclass(frozen=True)
class DeliberationRecord:
    deliberation_id: str
    proposal_id: str
    participants: int

    def __post_init__(self):
        if not self.deliberation_id:
            raise ValueError("deliberation_id is required")

        if not self.proposal_id:
            raise ValueError("proposal_id is required")

        if self.participants <= 0:
            raise ValueError("participants must be positive")
