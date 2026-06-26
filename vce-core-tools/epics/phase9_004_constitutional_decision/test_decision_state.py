from epics.phase9_004_constitutional_decision.decision_record import (
    DecisionRecord,
)
from epics.phase9_004_constitutional_decision.decision_state import (
    DecisionState,
)


def test_builds_decision_state():
    records = [
        DecisionRecord(
            "decision.001",
            "proposal.001",
            "accepted",
        ),
        DecisionRecord(
            "decision.002",
            "proposal.002",
            "rejected",
        ),
    ]

    state = DecisionState.from_records(records)

    assert state.total_decisions == 2
    assert state.accepted == 1
    assert state.rejected == 1


def test_empty_state():
    state = DecisionState.from_records([])

    assert state.total_decisions == 0
    assert state.accepted == 0
    assert state.rejected == 0
