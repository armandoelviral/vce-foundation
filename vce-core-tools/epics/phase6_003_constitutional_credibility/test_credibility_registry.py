from epics.phase6_003_constitutional_credibility.credibility_record import (
    CredibilityRecord,
)
from epics.phase6_003_constitutional_credibility.credibility_registry import (
    CredibilityRegistry,
)


def test_registry_adds_record():
    registry = CredibilityRegistry()

    record = CredibilityRecord(
        "cred.001",
        "identity.001",
        10,
    )

    registry.add(record)

    assert registry.records() == [record]
