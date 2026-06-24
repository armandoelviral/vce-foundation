from epics.phase6_005_constitutional_trust_score.trust_score_record import (
    TrustScoreRecord,
)
from epics.phase6_005_constitutional_trust_score.trust_score_state import (
    TrustScoreState,
)


def test_builds_trust_score_state():
    records = [
        TrustScoreRecord(
            "score.001",
            "identity.001",
            75,
        ),
        TrustScoreRecord(
            "score.002",
            "identity.001",
            85,
        ),
    ]

    state = TrustScoreState.from_records(records)

    assert state.total_records == 2
    assert state.average_score == 80


def test_empty_trust_score_state():
    state = TrustScoreState.from_records([])

    assert state.total_records == 0
    assert state.average_score == 0
