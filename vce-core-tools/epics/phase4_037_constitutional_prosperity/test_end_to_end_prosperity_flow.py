from epics.phase4_037_constitutional_prosperity.prosperity_loss import (
    ProsperityLossRecord,
)
from epics.phase4_037_constitutional_prosperity.prosperity_record import (
    ProsperityRecord,
)
from epics.phase4_037_constitutional_prosperity.prosperity_registry import (
    ProsperityRegistry,
)
from epics.phase4_037_constitutional_prosperity.prosperity_state import (
    ProsperityState,
)
from epics.phase4_037_constitutional_prosperity.prosperity_verifier import (
    verify_prosperity_state,
)


def test_end_to_end_prosperity_flow():
    registry = ProsperityRegistry()

    registry.add(
        ProsperityRecord(
            prosperity_id="prosperity.001",
            source_id="sustainability.001",
            prosperity_amount=100,
            rationale="durable growth",
        )
    )

    loss = ProsperityLossRecord(
        loss_id="loss.001",
        prosperity_id="prosperity.001",
        loss_amount=40,
        reason="economic contraction",
    )

    state = ProsperityState.from_records(
        prosperity_records=registry.records(),
        losses=[loss],
    )

    verification = verify_prosperity_state(state)

    assert verification["verified"] is True
    assert verification["net_prosperity"] == 60
