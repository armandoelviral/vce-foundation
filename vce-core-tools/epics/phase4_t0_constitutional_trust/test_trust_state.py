from epics.phase4_t0_constitutional_trust.trust_loss import (
    TrustLossRecord,
)
from epics.phase4_t0_constitutional_trust.trust_record import (
    TrustRecord,
)
from epics.phase4_t0_constitutional_trust.trust_state import (
    TrustState,
)


def test_builds_trust_state():
    trust = [
        TrustRecord(
            trust_id="trust.001",
            actor_id="citizen.alpha",
            trust_amount=100,
            source_reference="evidence.001",
        )
    ]

    losses = [
        TrustLossRecord(
            loss_id="loss.001",
            actor_id="citizen.alpha",
            trust_loss_amount=40,
            reason="violation",
        )
    ]

    state = TrustState.from_records(
        trust_records=trust,
        trust_losses=losses,
    )

    assert state.net_trust == 60


def test_empty_state():
    state = TrustState.from_records([], [])

    assert state.net_trust == 0
