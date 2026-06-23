from phase4.constitutional_economy_layer.capital_flow import (
    CapitalFlow,
)


def test_generates_flow():

    result = CapitalFlow.generate()

    assert "record" in result
    assert "registry" in result
    assert "accrual" in result
    assert "loss" in result
    assert "delegation" in result
    assert "state" in result
    assert "valid" in result


def test_balance_calculation():

    result = CapitalFlow.generate()

    assert (
        result["state"]["balance"]
        == 90
    )


def test_capital_valid():

    result = CapitalFlow.generate()

    assert result["valid"] is True
