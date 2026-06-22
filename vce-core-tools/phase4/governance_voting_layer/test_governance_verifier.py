from phase4.governance_voting_layer.governance_verifier import (
    GovernanceVerifier,
)


class MockState:

    def __init__(self, governance_state):
        self.governance_state = governance_state


def test_stable_state():

    state = MockState("STABLE")

    assert GovernanceVerifier.verify(state) is True


def test_updated_state():

    state = MockState("UPDATED")

    assert GovernanceVerifier.verify(state) is True


def test_under_review_state():

    state = MockState("UNDER_REVIEW")

    assert GovernanceVerifier.verify(state) is False
