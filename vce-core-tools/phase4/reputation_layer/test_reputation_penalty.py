from phase4.reputation_layer.reputation_penalty import (
    ReputationPenalty,
)


def test_contains_did():

    penalty = ReputationPenalty(
        citizen_did="did:tcn:test:01",
        penalty_reason="response_invalidity",
        penalty_points=-20,
    )

    assert penalty.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_reason():

    penalty = ReputationPenalty(
        citizen_did="did:tcn:test:01",
        penalty_reason="response_invalidity",
        penalty_points=-20,
    )

    assert penalty.penalty_reason == (
        "response_invalidity"
    )


def test_contains_points():

    penalty = ReputationPenalty(
        citizen_did="did:tcn:test:01",
        penalty_reason="response_invalidity",
        penalty_points=-20,
    )

    assert penalty.penalty_points == -20


def test_serializes():

    penalty = ReputationPenalty(
        citizen_did="did:tcn:test:01",
        penalty_reason="response_invalidity",
        penalty_points=-20,
    )

    assert penalty.to_dict() == {
        "citizen_did":
            "did:tcn:test:01",
        "penalty_reason":
            "response_invalidity",
        "penalty_points":
            -20,
    }
