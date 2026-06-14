from epics.ztc15_witness_suspension_recovery.recovery_record import (
    RecoveryRecord,
)

from epics.ztc15_witness_suspension_recovery.recovery_registry import (
    RecoveryRegistry,
)


def test_registry_stores_recovery_record():

    registry = RecoveryRegistry()

    record = RecoveryRecord(
        witness_id="witness-001",
        recovery_reason="key_rotation_completed",
    )

    registry.add(record)

    assert registry.count() == 1


def test_registry_reports_recovered_witness():

    registry = RecoveryRegistry()

    record = RecoveryRecord(
        witness_id="witness-001",
        recovery_reason="key_rotation_completed",
    )

    registry.add(record)

    assert registry.is_recovered(
        "witness-001"
    )


def test_registry_returns_false_for_unknown_witness():

    registry = RecoveryRegistry()

    assert not registry.is_recovered(
        "witness-999"
    )
