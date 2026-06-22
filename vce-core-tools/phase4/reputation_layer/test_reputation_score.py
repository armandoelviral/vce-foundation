from phase4.reputation_layer.reputation_score import (
    ReputationScore,
)


def test_contains_did():

    score = ReputationScore(
        citizen_did="did:tcn:test:01",
        score=120,
    )

    assert score.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_score():

    score = ReputationScore(
        citizen_did="did:tcn:test:01",
        score=120,
    )

    assert score.score == 120


def test_serializes():

    score = ReputationScore(
        citizen_did="did:tcn:test:01",
        score=120,
    )

    assert score.to_dict() == {
        "citizen_did":
            "did:tcn:test:01",
        "score":
            120,
    }
