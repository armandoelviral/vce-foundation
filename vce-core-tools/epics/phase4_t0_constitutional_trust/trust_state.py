from dataclasses import dataclass

from epics.phase4_t0_constitutional_trust.trust_loss import (
    TrustLossRecord,
)
from epics.phase4_t0_constitutional_trust.trust_record import (
    TrustRecord,
)


@dataclass(frozen=True)
class TrustState:
    total_trust: int
    total_loss: int
    net_trust: int

    @classmethod
    def from_records(
        cls,
        trust_records,
        trust_losses,
    ):
        total_trust = sum(
            r.trust_amount
            for r in trust_records
        )

        total_loss = sum(
            l.trust_loss_amount
            for l in trust_losses
        )

        return cls(
            total_trust=total_trust,
            total_loss=total_loss,
            net_trust=(
                total_trust - total_loss
            ),
        )
