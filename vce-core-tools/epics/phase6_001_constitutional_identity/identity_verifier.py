from epics.phase6_001_constitutional_identity.identity_state import (
    IdentityState,
)


def verify_identity_state(
    state: IdentityState,
):
    return {
        "verified": state.total_identities > 0,
        "total_identities": state.total_identities,
    }
