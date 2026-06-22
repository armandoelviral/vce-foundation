from phase4.governance_voting_layer.governance_state import (
    GovernanceState,
)


def test_contains_state():

    state = GovernanceState(
        governance_state="STABLE",
    )

    assert (
        state.governance_state
        == "STABLE"
    )


def test_serializes():

    state = GovernanceState(
        governance_state="STABLE",
    )

    assert state.to_dict() == {
        "governance_state":
            "STABLE",
    }


def test_updated_state():

    state = GovernanceState(
        governance_state="UPDATED",
    )

    assert (
        state.governance_state
        == "UPDATED"
    )

