from epics.phase9_005_constitutional_delegation.delegation_record import (
    DelegationRecord,
)
from epics.phase9_005_constitutional_delegation.delegation_state import (
    DelegationState,
)


def test_builds_delegation_state():
    records = [
        DelegationRecord(
            "delegation.001",
            "decision.001",
            "runtime.executor",
        ),
        DelegationRecord(
            "delegation.002",
            "decision.002",
            "audit.executor",
        ),
    ]

    state = DelegationState.from_records(records)

    assert state.total_delegations == 2
    assert state.unique_assignees == 2


def test_empty_state():
    state = DelegationState.from_records([])

    assert state.total_delegations == 0
    assert state.unique_assignees == 0
