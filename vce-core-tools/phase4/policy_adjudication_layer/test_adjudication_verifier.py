from phase4.policy_adjudication_layer.adjudication_verifier import (
    AdjudicationVerifier,
)


class MockState:

    def __init__(
        self,
        adjudication_state,
    ):
        self.adjudication_state = (
            adjudication_state
        )


def test_resolved_state():

    state = MockState(
        "RESOLVED",
    )

    assert (
        AdjudicationVerifier.verify(
            state
        )
        is True
    )


def test_open_state():

    state = MockState(
        "OPEN",
    )

    assert (
        AdjudicationVerifier.verify(
            state
        )
        is False
    )


def test_under_review_state():

    state = MockState(
        "UNDER_REVIEW",
    )

    assert (
        AdjudicationVerifier.verify(
            state
        )
        is False
    )
