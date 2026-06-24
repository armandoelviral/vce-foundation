from epics.phase4_t0_constitutional_trust.trust_record import (
    TrustRecord,
)
from epics.phase4_t0_constitutional_trust.trust_registry import (
    TrustRegistry,
)


def test_registry_stores_trust_record():
    registry = TrustRegistry()

    record = TrustRecord(
        trust_id="trust.001",
        actor_id="citizen.alpha",
        trust_amount=100,
        source_reference="evidence.001",
    )

    registry.add(record)

    assert registry.records() == [record]


def test_registry_rejects_duplicate_trust():
    registry = TrustRegistry()

    record = TrustRecord(
        trust_id="trust.001",
        actor_id="citizen.alpha",
        trust_amount=100,
        source_reference="evidence.001",
    )

    registry.add(record)

    try:
        registry.add(record)
        assert False
    except ValueError as exc:
        assert "duplicate trust" in str(exc)


def test_registry_returns_copy():
    registry = TrustRegistry()

    record = TrustRecord(
        trust_id="trust.001",
        actor_id="citizen.alpha",
        trust_amount=100,
        source_reference="evidence.001",
    )

    registry.add(record)

    records = registry.records()

    records.clear()

    assert len(registry.records()) == 1
