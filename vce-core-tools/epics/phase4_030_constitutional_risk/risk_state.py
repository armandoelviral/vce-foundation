from dataclasses import dataclass

from epics.phase4_030_constitutional_risk.risk_event import (
    RiskEventRecord,
)
from epics.phase4_030_constitutional_risk.risk_record import (
    RiskRecord,
)


@dataclass(frozen=True)
class RiskState:
    total_exposure: int
    total_impact: int
    remaining_exposure: int

    @classmethod
    def from_records(
        cls,
        risks: list[RiskRecord],
        events: list[RiskEventRecord],
    ):
        total_exposure = sum(risk.exposure_amount for risk in risks)
        total_impact = sum(event.impact_amount for event in events)

        return cls(
            total_exposure=total_exposure,
            total_impact=total_impact,
            remaining_exposure=total_exposure - total_impact,
        )
