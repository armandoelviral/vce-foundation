from epics.phase6_002_constitutional_reputation.reputation_record import (
    ReputationRecord,
)
from epics.phase6_002_constitutional_reputation.reputation_state import (
    ReputationState,
)


def test_builds_reputation_state():
    records = [
        ReputationRecord(
            "rep.001",
            "identity.001",
            10,
        ),
        ReputationRecord(
            "rep.002",
            "identity.001",
            20,
        ),
    ]

    state = ReputationState.from_records(records)

    assert state.total_records == 2
    assert state.total_score == 30


def test_empty_state():
    state = ReputationState.from_records([])

    assert state.total_records == 0
    assert state.total_score == 0
