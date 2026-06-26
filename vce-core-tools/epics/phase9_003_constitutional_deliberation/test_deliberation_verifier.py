from epics.phase9_003_constitutional_deliberation.deliberation_state import (
    DeliberationState,
)
from epics.phase9_003_constitutional_deliberation.deliberation_verifier import (
    verify_deliberation,
)


def test_deliberation_verified():
    state = DeliberationState(
        total_deliberations=2,
        total_participants=12,
    )

    result = verify_deliberation(state)

    assert result["verified"] is True


def test_empty_deliberation_not_verified():
    state = DeliberationState(
        total_deliberations=0,
        total_participants=0,
    )

    result = verify_deliberation(state)

    assert result["verified"] is False
