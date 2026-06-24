from epics.phase6_004_constitutional_trust_engine.trust_record import (
    TrustRecord,
)
from epics.phase6_004_constitutional_trust_engine.trust_registry import (
    TrustRegistry,
)


def test_registry_adds_record():
    registry = TrustRegistry()

    record = TrustRecord(
        "trust.001",
        "identity.001",
        25,
    )

    registry.add(record)

    assert registry.records() == [record]
