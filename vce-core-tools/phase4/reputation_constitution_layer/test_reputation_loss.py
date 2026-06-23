from phase4.reputation_constitution_layer.reputation_loss import (
    ReputationLoss,
)


def test_contains_identity():

    loss = ReputationLoss(
        identity_id="identity-001",
        points=5,
    )

    assert loss.identity_id == "identity-001"


def test_contains_points():

    loss = ReputationLoss(
        identity_id="identity-001",
        points=5,
    )

    assert loss.points == 5


def test_serializes():

    loss = ReputationLoss(
        identity_id="identity-001",
        points=5,
    )

    assert loss.to_dict() == {
        "identity_id": "identity-001",
        "points": 5,
    }
