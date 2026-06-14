from epics.ztc15_witness_suspension_recovery.witness_suspension_record import (
    WitnessSuspensionRecord,
)

from epics.ztc15_witness_suspension_recovery.suspension_registry import (
    SuspensionRegistry,
)


def test_registry_stores_record():

    registry = SuspensionRegistry()

    record = WitnessSuspensionRecord(
        witness_id="witness-001",
        reason="vote_divergence",
    )

    registry.add(record)

    assert registry.count() == 1


def test_registry_reports_suspended_witness():

    registry = SuspensionRegistry()

    record = WitnessSuspensionRecord(
        witness_id="witness-001",
        reason="vote_divergence",
    )

    registry.add(record)

    assert registry.is_suspended(
        "witness-001"
    )


def test_registry_returns_false_for_unknown_witness():

    registry = SuspensionRegistry()

    assert not registry.is_suspended(
        "witness-999"
    )
