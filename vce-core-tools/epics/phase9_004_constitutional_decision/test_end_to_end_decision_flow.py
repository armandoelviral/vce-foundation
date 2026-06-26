from epics.phase9_004_constitutional_decision.decision_record import (
    DecisionRecord,
)
from epics.phase9_004_constitutional_decision.decision_registry import (
    DecisionRegistry,
)
from epics.phase9_004_constitutional_decision.decision_state import (
    DecisionState,
)
from epics.phase9_004_constitutional_decision.decision_verifier import (
    verify_decisions,
)


def test_end_to_end_decision_flow():
    registry = DecisionRegistry()

    registry.add(
        DecisionRecord(
            "decision.001",
            "proposal.001",
            "accepted",
        )
    )

    registry.add(
        DecisionRecord(
            "decision.002",
            "proposal.002",
            "rejected",
        )
    )

    state = DecisionState.from_records(
        registry.records()
    )

    verification = verify_decisions(state)

    assert verification["verified"] is True
    assert verification["accepted"] == 1
    assert verification["rejected"] == 1
    assert verification["total_decisions"] == 2
