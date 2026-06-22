from phase4.governance_voting_layer.voting_right import (
    VotingRight,
)


def test_contains_did():

    voting_right = VotingRight(
        citizen_did="did:tcn:test:01",
        voting_right=True,
    )

    assert (
        voting_right.citizen_did
        == "did:tcn:test:01"
    )


def test_contains_right():

    voting_right = VotingRight(
        citizen_did="did:tcn:test:01",
        voting_right=True,
    )

    assert (
        voting_right.voting_right
        is True
    )


def test_serializes():

    voting_right = VotingRight(
        citizen_did="did:tcn:test:01",
        voting_right=True,
    )

    assert voting_right.to_dict() == {
        "citizen_did":
            "did:tcn:test:01",
        "voting_right":
            True,
    }
