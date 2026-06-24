from epics.phase6_003_constitutional_credibility.credibility_state import (
    CredibilityState,
)
from epics.phase6_003_constitutional_credibility.credibility_verifier import (
    verify_credibility,
)


def test_positive_credibility_verified():
    state = CredibilityState(
        total_records=2,
        total_score=30,
    )

    result = verify_credibility(state)

    assert result["verified"] is True


def test_zero_credibility_not_verified():
    state = CredibilityState(
        total_records=0,
        total_score=0,
    )

    result = verify_credibility(state)

    assert result["verified"] is False
