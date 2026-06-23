from epics.phase4_030_constitutional_risk.risk_record import (
    RiskRecord,
)
from epics.phase4_030_constitutional_risk.risk_registry import (
    RiskRegistry,
)


def test_registry_stores_risk_record():
    registry = RiskRegistry()

    record = RiskRecord(
        risk_id="risk.001",
        actor_id="institution.alpha",
        exposure_amount=100,
        source_reference="credit.001",
        reason="credit exposure",
    )

    registry.add(record)

    assert registry.records() == [record]


def test_registry_rejects_duplicate_risk():
    registry = RiskRegistry()

    record = RiskRecord(
        risk_id="risk.001",
        actor_id="institution.alpha",
        exposure_amount=100,
        source_reference="credit.001",
        reason="credit exposure",
    )

    registry.add(record)

    try:
        registry.add(record)
        assert False
    except ValueError as exc:
        assert "duplicate risk" in str(exc)


def test_registry_returns_copy():
    registry = RiskRegistry()

    record = RiskRecord(
        risk_id="risk.001",
        actor_id="institution.alpha",
        exposure_amount=100,
        source_reference="credit.001",
        reason="credit exposure",
    )

    registry.add(record)

    records = registry.records()
    records.clear()

    assert len(registry.records()) == 1
