from phase3.governance_escalation.escalation_record import (
    EscalationRecord,
)

from phase3.governance_escalation.escalation_registry import (
    EscalationRegistry,
)

from phase3.governance_escalation.escalation_query import (
    EscalationQuery,
)


def test_query_returns_record():

    registry = EscalationRegistry()

    record = EscalationRecord(
        escalation_id="esc-001",
        reason="quorum_failure",
        severity="HIGH",
    )

    registry.add(record)

    query = EscalationQuery(registry)

    result = query.by_id(
        "esc-001"
    )

    assert result == record


def test_query_returns_none_for_missing():

    registry = EscalationRegistry()

    query = EscalationQuery(registry)

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_severity():

    registry = EscalationRegistry()

    record = EscalationRecord(
        escalation_id="esc-001",
        reason="quorum_failure",
        severity="HIGH",
    )

    registry.add(record)

    query = EscalationQuery(registry)

    result = query.by_id(
        "esc-001"
    )

    assert result.severity == "HIGH"
