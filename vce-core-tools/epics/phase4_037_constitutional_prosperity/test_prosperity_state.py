from epics.phase4_037_constitutional_prosperity.prosperity_loss import (
    ProsperityLossRecord,
)
from epics.phase4_037_constitutional_prosperity.prosperity_record import (
    ProsperityRecord,
)
from epics.phase4_037_constitutional_prosperity.prosperity_state import (
    ProsperityState,
)


def test_builds_prosperity_state():
    records = [
        ProsperityRecord(
            "prosperity.001",
            "sustainability.001",
            100,
            "growth",
        )
    ]

    losses = [
        ProsperityLossRecord(
            "loss.001",
            "prosperity.001",
            40,
            "economic contraction",
        )
    ]

    state = ProsperityState.from_records(
        prosperity_records=records,
        losses=losses,
    )

    assert state.total_prosperity == 100
    assert state.total_loss == 40
    assert state.net_prosperity == 60


def test_empty_prosperity_state():
    state = ProsperityState.from_records([], [])

    assert state.net_prosperity == 0
