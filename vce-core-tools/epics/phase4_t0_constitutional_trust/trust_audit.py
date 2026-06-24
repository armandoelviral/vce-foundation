from epics.phase4_t0_constitutional_trust.trust_loss import (
    TrustLossRecord,
)
from epics.phase4_t0_constitutional_trust.trust_record import (
    TrustRecord,
)


def audit_trust(
    trust_records: list[TrustRecord],
    trust_losses: list[TrustLossRecord],
):
    return {
        "total_trust": sum(
            record.trust_amount
            for record in trust_records
        ),
        "total_loss": sum(
            loss.trust_loss_amount
            for loss in trust_losses
        ),
    }
