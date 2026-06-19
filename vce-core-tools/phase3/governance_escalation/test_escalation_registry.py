from phase3.governance_escalation.escalation_record import (
    EscalationRecord,
)

from phase3.governance_escalation.escalation_registry import (
    EscalationRegistry,
)


def test_registry_starts_empty():

    registry = EscalationRegistry()

    assert registry.count() == 0


def test_registry_accepts_record():

    registry = EscalationRegistry()

    record = EscalationRecord(
        escalation_id="esc-001",
        reason="quorum_failure",
        severity="HIGH",
    )

    registry.add(record)

    assert registry.count() == 1


def test_registry_returns_record():

    registry = EscalationRegistry()

    record = EscalationRecord(
        escalation_id="esc-001",
        reason="quorum_failure",
        severity="HIGH",
    )

    registry.add(record)

    recovered = registry.get(
        "esc-001"
    )

    assert recovered == record


def test_missing_record_returns_none():

    registry = EscalationRegistry()

    assert registry.get(
        "missing"
    ) is None
