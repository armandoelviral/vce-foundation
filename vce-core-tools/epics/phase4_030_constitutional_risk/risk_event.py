from dataclasses import dataclass


@dataclass(frozen=True)
class RiskEventRecord:
    event_id: str
    risk_id: str
    impact_amount: int
    reason: str

    def __post_init__(self):
        if not self.event_id:
            raise ValueError("event_id is required")

        if not self.risk_id:
            raise ValueError("risk_id is required")

        if self.impact_amount <= 0:
            raise ValueError("impact_amount must be positive")

        if not self.reason:
            raise ValueError("reason is required")
