from phase3.governance_recovery.recovery_record import (
    RecoveryRecord,
)

from phase3.governance_recovery.recovery_registry import (
    RecoveryRegistry,
)


def test_registry_starts_empty():

    registry = RecoveryRegistry()

    assert registry.count() == 0


def test_registry_accepts_record():

    registry = RecoveryRegistry()

    record = RecoveryRecord(
        recovery_id="rec-001",
        incident_id="esc-001",
        recovery_reason="manual_remediation",
    )

    registry.add(
        record
    )

    assert registry.count() == 1


def test_registry_returns_record():

    registry = RecoveryRegistry()

    record = RecoveryRecord(
        recovery_id="rec-001",
        incident_id="esc-001",
        recovery_reason="manual_remediation",
    )

    registry.add(
        record
    )

    recovered = registry.get(
        "rec-001"
    )

    assert recovered == record


def test_missing_record_returns_none():

    registry = RecoveryRegistry()

    assert registry.get(
        "missing"
    ) is None


def test_registry_lists_records():

    registry = RecoveryRegistry()

    registry.add(
        RecoveryRecord(
            recovery_id="rec-001",
            incident_id="esc-001",
            recovery_reason="manual_remediation",
        )
    )

    registry.add(
        RecoveryRecord(
            recovery_id="rec-002",
            incident_id="esc-002",
            recovery_reason="automatic_recovery",
        )
    )

    assert registry.recovery_ids() == [
        "rec-001",
        "rec-002",
    ]
