from epics.phase4_030_constitutional_risk.risk_record import (
    RiskRecord,
)


def calculate_total_exposure(
    records: list[RiskRecord],
) -> int:
    return sum(
        record.exposure_amount
        for record in records
    )
