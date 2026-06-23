from phase4.constitutional_economy_layer.capital_accrual import (
    CapitalAccrual,
)


def test_contains_identity():

    accrual = CapitalAccrual(
        identity_id="identity-001",
        amount=25,
    )

    assert accrual.identity_id == "identity-001"


def test_contains_amount():

    accrual = CapitalAccrual(
        identity_id="identity-001",
        amount=25,
    )

    assert accrual.amount == 25


def test_serializes():

    accrual = CapitalAccrual(
        identity_id="identity-001",
        amount=25,
    )

    assert accrual.to_dict() == {
        "identity_id": "identity-001",
        "amount": 25,
    }
