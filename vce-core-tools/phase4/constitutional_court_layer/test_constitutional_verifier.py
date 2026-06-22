from phase4.constitutional_court_layer.constitutional_verifier import (
    ConstitutionalVerifier,
)


class MockState:

    def __init__(self, constitutional_state):
        self.constitutional_state = constitutional_state


def test_active_state():

    state = MockState("ACTIVE")

    assert ConstitutionalVerifier.verify(state) is True


def test_upheld_state():

    state = MockState("UPHELD")

    assert ConstitutionalVerifier.verify(state) is True


def test_under_review_state():

    state = MockState("UNDER_REVIEW")

    assert ConstitutionalVerifier.verify(state) is False


def test_invalidated_state():

    state = MockState("INVALIDATED")

    assert ConstitutionalVerifier.verify(state) is False
