from dataclasses import dataclass

from epics.phase4_035_constitutional_stability.stability_loss import (
    StabilityLossRecord,
)
from epics.phase4_035_constitutional_stability.stability_record import (
    StabilityRecord,
)


@dataclass(frozen=True)
class StabilityState:
    total_stability: int
    total_loss: int
    net_stability: int

    @classmethod
    def from_records(
        cls,
        stability_records: list[StabilityRecord],
        losses: list[StabilityLossRecord],
    ):
        total_stability = sum(
            record.stability_amount for record in stability_records
        )
        total_loss = sum(loss.loss_amount for loss in losses)

        return cls(
            total_stability=total_stability,
            total_loss=total_loss,
            net_stability=total_stability - total_loss,
        )
