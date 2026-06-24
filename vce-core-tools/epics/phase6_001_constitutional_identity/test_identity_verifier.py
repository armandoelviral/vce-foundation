from epics.phase6_001_constitutional_identity.identity_state import (
    IdentityState,
)
from epics.phase6_001_constitutional_identity.identity_verifier import (
    verify_identity_state,
)


def test_identity_verification_succeeds():
    state = IdentityState(
        total_identities=1,
    )

    result = verify_identity_state(state)

    assert result["verified"] is True


def test_identity_verification_fails_when_empty():
    state = IdentityState(
        total_identities=0,
    )

    result = verify_identity_state(state)

    assert result["verified"] is False
