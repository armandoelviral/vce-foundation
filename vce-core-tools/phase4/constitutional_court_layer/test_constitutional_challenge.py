from phase4.constitutional_court_layer.constitutional_challenge import (
    ConstitutionalChallenge,
)


def test_contains_challenge_id():

    challenge = ConstitutionalChallenge(
        challenge_id="challenge-001",
        amendment_id="amendment-001",
    )

    assert (
        challenge.challenge_id
        == "challenge-001"
    )


def test_contains_amendment_id():

    challenge = ConstitutionalChallenge(
        challenge_id="challenge-001",
        amendment_id="amendment-001",
    )

    assert (
        challenge.amendment_id
        == "amendment-001"
    )


def test_serializes():

    challenge = ConstitutionalChallenge(
        challenge_id="challenge-001",
        amendment_id="amendment-001",
    )

    assert challenge.to_dict() == {
        "challenge_id":
            "challenge-001",
        "amendment_id":
            "amendment-001",
    }
