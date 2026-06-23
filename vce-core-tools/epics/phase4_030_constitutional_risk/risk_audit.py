from epics.phase4_030_constitutional_risk.risk_event import (
    RiskEventRecord,
)
from epics.phase4_030_constitutional_risk.risk_record import (
    RiskRecord,
)


def audit_risk_system(
    risks: list[RiskRecord],
    events: list[RiskEventRecord],
) -> dict:
    return {
        "risk_count": len(risks),
        "event_count": len(events),
        "total_exposure": sum(risk.exposure_amount for risk in risks),
        "total_impact": sum(event.impact_amount for event in events),
    }
