from epics.phase4_036_constitutional_sustainability.sustainability_depletion import (
    SustainabilityDepletionRecord,
)
from epics.phase4_036_constitutional_sustainability.sustainability_record import (
    SustainabilityRecord,
)
from epics.phase4_036_constitutional_sustainability.sustainability_state import (
    SustainabilityState,
)


def test_builds_sustainability_state():
    records = [
        SustainabilityRecord(
            sustainability_id="sus.001",
            source_id="stability.001",
            sustainability_amount=100,
            rationale="long-term continuity",
        )
    ]

    depletions = [
        SustainabilityDepletionRecord(
            depletion_id="depletion.001",
            sustainability_id="sus.001",
            depletion_amount=40,
            reason="resource exhaustion",
        )
    ]

    state = SustainabilityState.from_records(
        sustainability_records=records,
        depletions=depletions,
    )

    assert state.total_sustainability == 100
    assert state.total_depletion == 40
    assert state.net_sustainability == 60


def test_empty_sustainability_state():
    state = SustainabilityState.from_records([], [])

    assert state.total_sustainability == 0
    assert state.total_depletion == 0
    assert state.net_sustainability == 0
