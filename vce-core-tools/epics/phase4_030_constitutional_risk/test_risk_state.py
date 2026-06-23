from epics.phase4_030_constitutional_risk.risk_event import (
    RiskEventRecord,
)
from epics.phase4_030_constitutional_risk.risk_record import (
    RiskRecord,
)
from epics.phase4_030_constitutional_risk.risk_state import (
    RiskState,
)


def test_builds_risk_state():
    risks = [
        RiskRecord(
            risk_id="risk.001",
            actor_id="institution.alpha",
            exposure_amount=100,
            source_reference="credit.001",
            reason="credit exposure",
        )
    ]

    events = [
        RiskEventRecord(
            event_id="event.001",
            risk_id="risk.001",
            impact_amount=40,
            reason="partial default realized",
        )
    ]

    state = RiskState.from_records(risks=risks, events=events)

    assert state.total_exposure == 100
    assert state.total_impact == 40
    assert state.remaining_exposure == 60


def test_empty_risk_state():
    state = RiskState.from_records(risks=[], events=[])

    assert state.total_exposure == 0
    assert state.total_impact == 0
    assert state.remaining_exposure == 0
