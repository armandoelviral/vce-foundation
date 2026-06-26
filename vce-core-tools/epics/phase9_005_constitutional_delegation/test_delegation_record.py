from epics.phase9_005_constitutional_delegation.delegation_record import (
    DelegationRecord,
)


def test_delegation_record_creation():
    record = DelegationRecord(
        delegation_id="delegation.001",
        decision_id="decision.001",
        assignee="runtime.executor",
    )

    assert record.delegation_id == "delegation.001"
    assert record.assignee == "runtime.executor"


def test_requires_delegation_id():
    try:
        DelegationRecord(
            "",
            "decision.001",
            "runtime.executor",
        )
        assert False
    except ValueError as exc:
        assert "delegation_id" in str(exc)
