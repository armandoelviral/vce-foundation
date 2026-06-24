from epics.phase4_035_constitutional_stability.stability_loss import (
    StabilityLossRecord,
)
from epics.phase4_035_constitutional_stability.stability_record import (
    StabilityRecord,
)
from epics.phase4_035_constitutional_stability.stability_state import (
    StabilityState,
)


def test_builds_stability_state():
    records = [StabilityRecord("s1", "treasury.001", 100, "continuity")]
    losses = [StabilityLossRecord("l1", "s1", 40, "liquidity shock")]

    state = StabilityState.from_records(records, losses)

    assert state.total_stability == 100
    assert state.total_loss == 40
    assert state.net_stability == 60


def test_empty_stability_state():
    state = StabilityState.from_records([], [])

    assert state.total_stability == 0
    assert state.total_loss == 0
    assert state.net_stability == 0
