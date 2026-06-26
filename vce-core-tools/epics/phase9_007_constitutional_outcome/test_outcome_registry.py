from epics.phase9_007_constitutional_outcome.outcome_record import (
    OutcomeRecord,
)
from epics.phase9_007_constitutional_outcome.outcome_registry import (
    OutcomeRegistry,
)


def test_registry_adds_outcome():
    registry = OutcomeRegistry()

    registry.add(
        OutcomeRecord(
            "outcome.001",
            "execution.001",
            "successful",
        )
    )

    assert len(registry.records()) == 1
