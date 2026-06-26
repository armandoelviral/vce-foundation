from epics.phase9_004_constitutional_decision.decision_record import (
    DecisionRecord,
)
from epics.phase9_004_constitutional_decision.decision_registry import (
    DecisionRegistry,
)


def test_registry_adds_decision():
    registry = DecisionRegistry()

    registry.add(
        DecisionRecord(
            "decision.001",
            "proposal.001",
            "accepted",
        )
    )

    assert len(registry.records()) == 1
