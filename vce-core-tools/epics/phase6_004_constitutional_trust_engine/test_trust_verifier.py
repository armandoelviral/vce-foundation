from epics.phase6_004_constitutional_trust_engine.trust_state import (
    TrustState,
)
from epics.phase6_004_constitutional_trust_engine.trust_verifier import (
    verify_trust,
)


def test_positive_trust_verified():
    state = TrustState(
        total_records=2,
        total_score=30,
    )

    result = verify_trust(state)

    assert result["verified"] is True


def test_zero_trust_not_verified():
    state = TrustState(
        total_records=0,
        total_score=0,
    )

    result = verify_trust(state)

    assert result["verified"] is False
