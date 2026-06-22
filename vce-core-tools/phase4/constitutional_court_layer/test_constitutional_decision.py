from phase4.constitutional_court_layer.constitutional_decision import (
    ConstitutionalDecision,
)


def test_contains_review_id():

    decision = ConstitutionalDecision(
        review_id="review-001",
        decision="UPHELD",
    )

    assert decision.review_id == (
        "review-001"
    )


def test_contains_decision():

    decision = ConstitutionalDecision(
        review_id="review-001",
        decision="UPHELD",
    )

    assert decision.decision == (
        "UPHELD"
    )


def test_serializes():

    decision = ConstitutionalDecision(
        review_id="review-001",
        decision="UPHELD",
    )

    assert decision.to_dict() == {
        "review_id":
            "review-001",
        "decision":
            "UPHELD",
    }
