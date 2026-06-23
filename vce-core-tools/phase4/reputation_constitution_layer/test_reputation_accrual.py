from phase4.reputation_constitution_layer.reputation_accrual import (
    ReputationAccrual,
)


def test_contains_identity_id():
    accrual = ReputationAccrual(
        identity_id="identity-001",
        points=10,
    )

    assert accrual.identity_id == "identity-001"


def test_contains_points():
    accrual = ReputationAccrual(
        identity_id="identity-001",
        points=10,
    )

    assert accrual.points == 10


def test_serializes():
    accrual = ReputationAccrual(
        identity_id="identity-001",
        points=10,
    )

    assert accrual.to_dict() == {
        "identity_id": "identity-001",
        "points": 10,
    }
