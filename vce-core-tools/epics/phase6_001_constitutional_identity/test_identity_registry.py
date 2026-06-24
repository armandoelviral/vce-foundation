from epics.phase6_001_constitutional_identity.identity_record import (
    IdentityRecord,
)
from epics.phase6_001_constitutional_identity.identity_registry import (
    IdentityRegistry,
)


def test_registry_adds_identity():
    registry = IdentityRegistry()

    record = IdentityRecord(
        "identity.001",
        "subject.001",
        "human",
    )

    registry.add(record)

    assert registry.records() == [record]


def test_registry_rejects_duplicate():
    registry = IdentityRegistry()

    record = IdentityRecord(
        "identity.001",
        "subject.001",
        "human",
    )

    registry.add(record)

    try:
        registry.add(record)
        assert False
    except ValueError as exc:
        assert "duplicate identity" in str(exc)


def test_registry_returns_copy():
    registry = IdentityRegistry()

    record = IdentityRecord(
        "identity.001",
        "subject.001",
        "human",
    )

    registry.add(record)

    items = registry.records()
    items.clear()

    assert registry.records() == [record]
