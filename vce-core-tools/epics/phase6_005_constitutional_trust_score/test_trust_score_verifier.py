from epics.phase6_005_constitutional_trust_score.trust_score_state import (
    TrustScoreState,
)
from epics.phase6_005_constitutional_trust_score.trust_score_verifier import (
    verify_trust_score,
)


def test_positive_score_verified():
    state = TrustScoreState(
        total_records=2,
        average_score=80,
    )

    result = verify_trust_score(state)

    assert result["verified"] is True


def test_zero_score_not_verified():
    state = TrustScoreState(
        total_records=0,
        average_score=0,
    )

    result = verify_trust_score(state)

    assert result["verified"] is False
