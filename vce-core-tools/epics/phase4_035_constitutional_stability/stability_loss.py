from dataclasses import dataclass


@dataclass(frozen=True)
class StabilityLossRecord:
    loss_id: str
    stability_id: str
    loss_amount: int
    reason: str

    def __post_init__(self):
        if not self.loss_id:
            raise ValueError("loss_id is required")

        if not self.stability_id:
            raise ValueError("stability_id is required")

        if self.loss_amount <= 0:
            raise ValueError("loss_amount must be positive")

        if not self.reason:
            raise ValueError("reason is required")
