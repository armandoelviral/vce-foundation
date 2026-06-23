from phase4.constitutional_economy_layer.capital_state import (
    CapitalState,
)


def test_contains_balance():

    state = CapitalState(
        balance=100,
    )

    assert state.balance == 100


def test_serializes():

    state = CapitalState(
        balance=100,
    )

    assert state.to_dict() == {
        "balance": 100,
    }


def test_supports_zero():

    state = CapitalState(
        balance=0,
    )

    assert state.balance == 0
