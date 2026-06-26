from epics.phase9_005_constitutional_delegation.delegation_assignment import (
    delegation_assigned,
)


def test_assignment_exists():
    assert delegation_assigned("runtime.executor") is True


def test_assignment_missing():
    assert delegation_assigned("") is False
