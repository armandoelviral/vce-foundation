from dataclasses import dataclass


@dataclass(frozen=True)
class TrustRecord:
    trust_id: str
    actor_id: str
    trust_amount: int
    source_reference: str

    def __post_init__(self):
        if not self.trust_id:
            raise ValueError("trust_id is required")

        if not self.actor_id:
            raise ValueError("actor_id is required")

        if self.trust_amount <= 0:
            raise ValueError("trust_amount must be positive")

        if not self.source_reference:
            raise ValueError("source_reference is required")
