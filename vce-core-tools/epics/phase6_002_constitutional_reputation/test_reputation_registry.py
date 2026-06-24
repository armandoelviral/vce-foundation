from epics.phase6_002_constitutional_reputation.reputation_record import (
    ReputationRecord,
)
from epics.phase6_002_constitutional_reputation.reputation_registry import (
    ReputationRegistry,
)


def test_registry_adds_record():
    registry = ReputationRegistry()

    record = ReputationRecord(
        "rep.001",
        "identity.001",
        10,
    )

    registry.add(record)

    assert registry.records() == [record]
