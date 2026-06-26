from epics.phase9_003_constitutional_deliberation.deliberation_state import (
    DeliberationState,
)


def verify_deliberation(
    state: DeliberationState,
):
    return {
        "verified": (
            state.total_deliberations > 0
            and state.total_participants > 0
        ),
        "total_deliberations": state.total_deliberations,
        "total_participants": state.total_participants,
    }
