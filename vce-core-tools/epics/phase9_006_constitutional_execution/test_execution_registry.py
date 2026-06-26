from epics.phase9_006_constitutional_execution.execution_record import (
    ExecutionRecord,
)
from epics.phase9_006_constitutional_execution.execution_registry import (
    ExecutionRegistry,
)


def test_registry_adds_execution():
    registry = ExecutionRegistry()

    registry.add(
        ExecutionRecord(
            "execution.001",
            "delegation.001",
            "completed",
        )
    )

    assert len(registry.records()) == 1
