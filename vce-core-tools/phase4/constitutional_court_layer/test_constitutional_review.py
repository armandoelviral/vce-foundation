from phase4.constitutional_court_layer.constitutional_review import (
    ConstitutionalReview,
)


def test_contains_review_id():

    review = ConstitutionalReview(
        review_id="review-001",
        challenge_id="challenge-001",
    )

    assert review.review_id == (
        "review-001"
    )


def test_contains_challenge_id():

    review = ConstitutionalReview(
        review_id="review-001",
        challenge_id="challenge-001",
    )

    assert review.challenge_id == (
        "challenge-001"
    )


def test_serializes():

    review = ConstitutionalReview(
        review_id="review-001",
        challenge_id="challenge-001",
    )

    assert review.to_dict() == {
        "review_id":
            "review-001",
        "challenge_id":
            "challenge-001",
    }
