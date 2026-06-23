from dataclasses import dataclass


@dataclass(frozen=True)
class RiskRecord:
    risk_id: str
    actor_id: str
    exposure_amount: int
    source_reference: str
    reason: str

    def __post_init__(self):
        if not self.risk_id:
            raise ValueError("risk_id is required")

        if not self.actor_id:
            raise ValueError("actor_id is required")

        if self.exposure_amount <= 0:
            raise ValueError("exposure_amount must be positive")

        if not self.source_reference:
            raise ValueError("source_reference is required")

        if not self.reason:
            raise ValueError("reason is required")
