from phase4.constitutional_court_layer.constitutional_state import (
    ConstitutionalState,
)


def test_contains_state():

    state = ConstitutionalState(
        constitutional_state="ACTIVE",
    )

    assert (
        state.constitutional_state
        == "ACTIVE"
    )


def test_serializes():

    state = ConstitutionalState(
        constitutional_state="ACTIVE",
    )

    assert state.to_dict() == {
        "constitutional_state":
            "ACTIVE",
    }


def test_review_state():

    state = ConstitutionalState(
        constitutional_state="UNDER_REVIEW",
    )

    assert (
        state.constitutional_state
        == "UNDER_REVIEW"
    )
