from dataclasses import dataclass


@dataclass(frozen=True)
class TrustLossRecord:
    loss_id: str
    actor_id: str
    trust_loss_amount: int
    reason: str

    def __post_init__(self):
        if not self.loss_id:
            raise ValueError("loss_id is required")

        if not self.actor_id:
            raise ValueError("actor_id is required")

        if self.trust_loss_amount <= 0:
            raise ValueError(
                "trust_loss_amount must be positive"
            )

        if not self.reason:
            raise ValueError("reason is required")
