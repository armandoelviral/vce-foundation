from phase3.governance_recovery.recovery_record import (
    RecoveryRecord,
)

from phase3.governance_recovery.recovery_registry import (
    RecoveryRegistry,
)

from phase3.governance_recovery.recovery_query import (
    RecoveryQuery,
)


def test_query_returns_record():

    registry = RecoveryRegistry()

    record = RecoveryRecord(
        recovery_id="rec-001",
        incident_id="esc-001",
        recovery_reason="manual_remediation",
    )

    registry.add(
        record
    )

    query = RecoveryQuery(
        registry
    )

    result = query.by_id(
        "rec-001"
    )

    assert result == record


def test_query_returns_none_for_missing():

    registry = RecoveryRegistry()

    query = RecoveryQuery(
        registry
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_reason():

    registry = RecoveryRegistry()

    record = RecoveryRecord(
        recovery_id="rec-001",
        incident_id="esc-001",
        recovery_reason="manual_remediation",
    )

    registry.add(
        record
    )

    query = RecoveryQuery(
        registry
    )

    result = query.by_id(
        "rec-001"
    )

    assert (
        result.recovery_reason
        == "manual_remediation"
    )
