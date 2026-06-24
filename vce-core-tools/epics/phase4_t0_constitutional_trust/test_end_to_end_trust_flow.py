from epics.phase4_t0_constitutional_trust.trust_loss import (
    TrustLossRecord,
)
from epics.phase4_t0_constitutional_trust.trust_record import (
    TrustRecord,
)
from epics.phase4_t0_constitutional_trust.trust_registry import (
    TrustRegistry,
)
from epics.phase4_t0_constitutional_trust.trust_state import (
    TrustState,
)
from epics.phase4_t0_constitutional_trust.trust_verifier import (
    verify_trust_state,
)


def test_end_to_end_trust_flow():
    registry = TrustRegistry()

    registry.add(
        TrustRecord(
            trust_id="trust.001",
            actor_id="citizen.alpha",
            trust_amount=100,
            source_reference="evidence.001",
        )
    )

    loss = TrustLossRecord(
        loss_id="loss.001",
        actor_id="citizen.alpha",
        trust_loss_amount=40,
        reason="constitutional violation",
    )

    state = TrustState.from_records(
        trust_records=registry.records(),
        trust_losses=[loss],
    )

    assert state.total_trust == 100
    assert state.total_loss == 40
    assert state.net_trust == 60

    verification = verify_trust_state(state)

    assert verification["verified"] is True
