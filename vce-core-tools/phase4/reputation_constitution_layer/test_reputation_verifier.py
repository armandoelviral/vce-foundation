from phase4.reputation_constitution_layer.reputation_verifier import (
    ReputationVerifier,
)


class MockState:

    def __init__(self, score):
        self.score = score


def test_positive_reputation():

    state = MockState(
        score=100,
    )

    assert ReputationVerifier.verify(
        state
    ) is True


def test_zero_reputation():

    state = MockState(
        score=0,
    )

    assert ReputationVerifier.verify(
        state
    ) is True


def test_negative_reputation():

    state = MockState(
        score=-1,
    )

    assert ReputationVerifier.verify(
        state
    ) is False
