from epics.phase4_037_constitutional_prosperity.prosperity_loss import (
    ProsperityLossRecord,
)
from epics.phase4_037_constitutional_prosperity.prosperity_record import (
    ProsperityRecord,
)


def audit_prosperity(
    prosperity_records: list[ProsperityRecord],
    losses: list[ProsperityLossRecord],
):
    return {
        "prosperity_count": len(prosperity_records),
        "loss_count": len(losses),
        "total_prosperity": sum(
            record.prosperity_amount
            for record in prosperity_records
        ),
        "total_loss": sum(
            loss.loss_amount
            for loss in losses
        ),
    }
