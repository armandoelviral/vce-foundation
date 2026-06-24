from dataclasses import dataclass

from epics.phase4_037_constitutional_prosperity.prosperity_loss import (
    ProsperityLossRecord,
)
from epics.phase4_037_constitutional_prosperity.prosperity_record import (
    ProsperityRecord,
)


@dataclass(frozen=True)
class ProsperityState:
    total_prosperity: int
    total_loss: int
    net_prosperity: int

    @classmethod
    def from_records(
        cls,
        prosperity_records: list[ProsperityRecord],
        losses: list[ProsperityLossRecord],
    ):
        total_prosperity = sum(
            record.prosperity_amount
            for record in prosperity_records
        )

        total_loss = sum(
            loss.loss_amount
            for loss in losses
        )

        return cls(
            total_prosperity=total_prosperity,
            total_loss=total_loss,
            net_prosperity=total_prosperity - total_loss,
        )
