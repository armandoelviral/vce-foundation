from epics.phase4_030_constitutional_risk.risk_event import (
    RiskEventRecord,
)
from epics.phase4_030_constitutional_risk.risk_record import (
    RiskRecord,
)
from epics.phase4_030_constitutional_risk.risk_registry import (
    RiskRegistry,
)
from epics.phase4_030_constitutional_risk.risk_state import (
    RiskState,
)
from epics.phase4_030_constitutional_risk.risk_verifier import (
    verify_risk_state,
)


def test_end_to_end_constitutional_risk_flow():
    registry = RiskRegistry()

    registry.add(
        RiskRecord(
            risk_id="risk.001",
            actor_id="institution.alpha",
            exposure_amount=100,
            source_reference="credit.001",
            reason="credit exposure",
        )
    )

    registry.add(
        RiskRecord(
            risk_id="risk.002",
            actor_id="institution.alpha",
            exposure_amount=50,
            source_reference="credit.002",
            reason="credit exposure",
        )
    )

    event = RiskEventRecord(
        event_id="event.001",
        risk_id="risk.001",
        impact_amount=40,
        reason="partial default realized",
    )

    state = RiskState.from_records(
        risks=registry.records(),
        events=[event],
    )

    assert state.total_exposure == 150
    assert state.total_impact == 40
    assert state.remaining_exposure == 110

    verification = verify_risk_state(state)

    assert verification["verified"] is True
