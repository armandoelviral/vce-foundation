from epics.phase4_t0_constitutional_trust.trust_state import (
    TrustState,
)
from epics.phase4_t0_constitutional_trust.trust_verifier import (
    verify_trust_state,
)


def test_trust_verification_succeeds():
    state = TrustState(
        total_trust=100,
        total_loss=40,
        net_trust=60,
    )

    result = verify_trust_state(state)

    assert result["verified"] is True


def test_trust_verification_fails():
    state = TrustState(
        total_trust=100,
        total_loss=150,
        net_trust=-50,
    )

    result = verify_trust_state(state)

    assert result["verified"] is False


def test_reports_net_trust():
    state = TrustState(
        total_trust=100,
        total_loss=20,
        net_trust=80,
    )

    result = verify_trust_state(state)

    assert result["net_trust"] == 80
