from epics.phase9_005_constitutional_delegation.delegation_record import (
    DelegationRecord,
)
from epics.phase9_005_constitutional_delegation.delegation_registry import (
    DelegationRegistry,
)


def test_registry_adds_delegation():
    registry = DelegationRegistry()

    registry.add(
        DelegationRecord(
            "delegation.001",
            "decision.001",
            "runtime.executor",
        )
    )

    assert len(registry.records()) == 1
