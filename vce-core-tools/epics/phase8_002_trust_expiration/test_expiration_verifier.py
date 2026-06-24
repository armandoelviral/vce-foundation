from epics.phase8_002_trust_expiration.expiration_state import (
    ExpirationState,
)
from epics.phase8_002_trust_expiration.expiration_verifier import (
    verify_expiration,
)


def test_expiration_verified():
    state = ExpirationState(
        total_records=2,
        total_remaining_days=395,
    )

    result = verify_expiration(state)

    assert result["verified"] is True


def test_empty_expiration_not_verified():
    state = ExpirationState(
        total_records=0,
        total_remaining_days=0,
    )

    result = verify_expiration(state)

    assert result["verified"] is False
