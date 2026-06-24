from epics.phase4_036_constitutional_sustainability.sustainability_depletion import (
    SustainabilityDepletionRecord,
)
from epics.phase4_036_constitutional_sustainability.sustainability_record import (
    SustainabilityRecord,
)
from epics.phase4_036_constitutional_sustainability.sustainability_registry import (
    SustainabilityRegistry,
)
from epics.phase4_036_constitutional_sustainability.sustainability_state import (
    SustainabilityState,
)
from epics.phase4_036_constitutional_sustainability.sustainability_verifier import (
    verify_sustainability_state,
)


def test_end_to_end_sustainability_flow():
    registry = SustainabilityRegistry()

    registry.add(
        SustainabilityRecord(
            sustainability_id="sus.001",
            source_id="stability.001",
            sustainability_amount=100,
            rationale="long-term continuity",
        )
    )

    depletion = SustainabilityDepletionRecord(
        depletion_id="depletion.001",
        sustainability_id="sus.001",
        depletion_amount=40,
        reason="resource exhaustion",
    )

    state = SustainabilityState.from_records(
        sustainability_records=registry.records(),
        depletions=[depletion],
    )

    assert state.total_sustainability == 100
    assert state.total_depletion == 40
    assert state.net_sustainability == 60

    verification = verify_sustainability_state(state)

    assert verification["verified"] is True
    assert verification["net_sustainability"] == 60

