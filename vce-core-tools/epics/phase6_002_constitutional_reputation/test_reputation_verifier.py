from epics.phase6_002_constitutional_reputation.reputation_state import (
    ReputationState,
)
from epics.phase6_002_constitutional_reputation.reputation_verifier import (
    verify_reputation,
)


def test_positive_reputation_verified():
    state = ReputationState(
        total_records=2,
        total_score=30,
    )

    result = verify_reputation(state)

    assert result["verified"] is True


def test_zero_reputation_not_verified():
    state = ReputationState(
        total_records=0,
        total_score=0,
    )

    result = verify_reputation(state)

    assert result["verified"] is False
