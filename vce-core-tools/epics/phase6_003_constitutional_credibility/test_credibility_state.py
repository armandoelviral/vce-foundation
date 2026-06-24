from epics.phase6_003_constitutional_credibility.credibility_record import (
    CredibilityRecord,
)
from epics.phase6_003_constitutional_credibility.credibility_state import (
    CredibilityState,
)


def test_builds_credibility_state():
    records = [
        CredibilityRecord("cred.001", "identity.001", 10),
        CredibilityRecord("cred.002", "identity.001", 20),
    ]

    state = CredibilityState.from_records(records)

    assert state.total_records == 2
    assert state.total_score == 30


def test_empty_credibility_state():
    state = CredibilityState.from_records([])

    assert state.total_records == 0
    assert state.total_score == 0
