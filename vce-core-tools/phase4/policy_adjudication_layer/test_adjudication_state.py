from phase4.policy_adjudication_layer.adjudication_state import (
    AdjudicationState,
)


def test_contains_state():

    state = AdjudicationState(
        adjudication_state="RESOLVED",
    )

    assert state.adjudication_state == "RESOLVED"


def test_serializes():

    state = AdjudicationState(
        adjudication_state="RESOLVED",
    )

    assert state.to_dict() == {
        "adjudication_state": "RESOLVED",
    }


def test_open_state():

    state = AdjudicationState(
        adjudication_state="OPEN",
    )

    assert state.adjudication_state == "OPEN"
