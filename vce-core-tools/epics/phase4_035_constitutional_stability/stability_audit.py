
from epics.phase4_035_constitutional_stability.stability_loss import (
    StabilityLossRecord,
)
from epics.phase4_035_constitutional_stability.stability_record import (
    StabilityRecord,
)


def audit_stability(
    stability_records: list[StabilityRecord],
    losses: list[StabilityLossRecord],
):
    return {
        "stability_count": len(stability_records),
        "loss_count": len(losses),
        "total_stability": sum(
            record.stability_amount for record in stability_records
        ),
        "total_loss": sum(loss.loss_amount for loss in losses),
    }
