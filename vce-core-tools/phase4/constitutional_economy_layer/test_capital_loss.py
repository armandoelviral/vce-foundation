from phase4.constitutional_economy_layer.capital_loss import (
    CapitalLoss,
)


def test_contains_identity():

    loss = CapitalLoss(
        identity_id="identity-001",
        amount=10,
    )

    assert loss.identity_id == "identity-001"


def test_contains_amount():

    loss = CapitalLoss(
        identity_id="identity-001",
        amount=10,
    )

    assert loss.amount == 10


def test_serializes():

    loss = CapitalLoss(
        identity_id="identity-001",
        amount=10,
    )

    assert loss.to_dict() == {
        "identity_id": "identity-001",
        "amount": 10,
    }
