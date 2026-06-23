from epics.phase4_030_constitutional_risk.risk_exposure import (
    calculate_total_exposure,
)
from epics.phase4_030_constitutional_risk.risk_record import (
    RiskRecord,
)


def test_calculates_total_exposure():
    records = [
        RiskRecord(
            risk_id="risk.001",
            actor_id="institution.alpha",
            exposure_amount=100,
            source_reference="credit.001",
            reason="credit",
        ),
        RiskRecord(
            risk_id="risk.002",
            actor_id="institution.alpha",
            exposure_amount=50,
            source_reference="credit.002",
            reason="credit",
        ),
    ]

    assert calculate_total_exposure(records) == 150


def test_empty_exposure():
    assert calculate_total_exposure([]) == 0


def test_single_exposure():
    records = [
        RiskRecord(
            risk_id="risk.001",
            actor_id="institution.alpha",
            exposure_amount=75,
            source_reference="credit.001",
            reason="credit",
        )
    ]

    assert calculate_total_exposure(records) == 75
