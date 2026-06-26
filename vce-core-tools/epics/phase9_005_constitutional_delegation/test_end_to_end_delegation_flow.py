from epics.phase9_005_constitutional_delegation.delegation_record import (
    DelegationRecord,
)
from epics.phase9_005_constitutional_delegation.delegation_registry import (
    DelegationRegistry,
)
from epics.phase9_005_constitutional_delegation.delegation_state import (
    DelegationState,
)
from epics.phase9_005_constitutional_delegation.delegation_verifier import (
    verify_delegation,
)


def test_end_to_end_delegation_flow():
    registry = DelegationRegistry()

    registry.add(
        DelegationRecord(
            "delegation.001",
            "decision.001",
            "runtime.executor",
        )
    )

    registry.add(
        DelegationRecord(
            "delegation.002",
            "decision.002",
            "audit.executor",
        )
    )

    state = DelegationState.from_records(
        registry.records()
    )

    verification = verify_delegation(state)

    assert verification["verified"] is True
    assert verification["total_delegations"] == 2
    assert verification["unique_assignees"] == 2
