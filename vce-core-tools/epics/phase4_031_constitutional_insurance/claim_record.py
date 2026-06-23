from dataclasses import dataclass


@dataclass(frozen=True)
class ClaimRecord:
    claim_id: str
    policy_id: str
    claim_amount: int
    reason: str

    def __post_init__(self):
        if not self.claim_id:
            raise ValueError("claim_id is required")

        if not self.policy_id:
            raise ValueError("policy_id is required")

        if self.claim_amount <= 0:
            raise ValueError("claim_amount must be positive")

        if not self.reason:
            raise ValueError("reason is required")
