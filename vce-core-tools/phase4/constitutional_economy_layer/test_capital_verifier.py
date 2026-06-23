from phase4.constitutional_economy_layer.capital_verifier import (
    CapitalVerifier,
)


class MockState:

    def __init__(self, balance):
        self.balance = balance


def test_positive_balance():

    state = MockState(
        balance=100,
    )

    assert CapitalVerifier.verify(
        state
    ) is True


def test_zero_balance():

    state = MockState(
        balance=0,
    )

    assert CapitalVerifier.verify(
        state
    ) is True


def test_negative_balance():

    state = MockState(
        balance=-1,
    )

    assert CapitalVerifier.verify(
        state
    ) is False
