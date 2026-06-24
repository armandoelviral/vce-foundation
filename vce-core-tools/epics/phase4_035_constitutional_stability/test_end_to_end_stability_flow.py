from epics.phase4_035_constitutional_stability.stability_loss import (
    StabilityLossRecord,
)
from epics.phase4_035_constitutional_stability.stability_record import (
    StabilityRecord,
)
from epics.phase4_035_constitutional_stability.stability_registry import (
    StabilityRegistry,
)
from epics.phase4_035_constitutional_stability.stability_state import (
    StabilityState,
)
from epics.phase4_035_constitutional_stability.stability_verifier import (
    verify_stability_state,
)


def test_end_to_end_stability_flow():
    registry = StabilityRegistry()

    registry.add(
        StabilityRecord(
            stability_id="stability.001",
            source_id="liquidity.001",
            stability_amount=100,
            rationale="constitutional continuity",
        )
    )

    loss = StabilityLossRecord(
        loss_id="loss.001",
        stability_id="stability.001",
        loss_amount=40,
        reason="liquidity shock",
    )

    state = StabilityState.from_records(
        stability_records=registry.records(),
        losses=[loss],
    )

    assert state.total_stability == 100
    assert state.total_loss == 40
    assert state.net_stability == 60

    verification = verify_stability_state(state)

    assert verification["verified"] is True
