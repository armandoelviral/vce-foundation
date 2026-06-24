from epics.phase8_002_trust_expiration.expiration_record import (
    ExpirationRecord,
)
from epics.phase8_002_trust_expiration.expiration_registry import (
    ExpirationRegistry,
)


def test_registry_adds_record():
    registry = ExpirationRegistry()

    record = ExpirationRecord(
        "exp.001",
        "trust.001",
        365,
    )

    registry.add(record)

    assert registry.records() == [record]
