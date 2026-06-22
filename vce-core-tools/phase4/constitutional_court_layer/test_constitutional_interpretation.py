from phase4.constitutional_court_layer.constitutional_interpretation import (
    ConstitutionalInterpretation,
)


def test_contains_review_id():

    interpretation = ConstitutionalInterpretation(
        review_id="review-001",
        interpretation="CONSISTENT",
    )

    assert (
        interpretation.review_id
        == "review-001"
    )


def test_contains_interpretation():

    interpretation = ConstitutionalInterpretation(
        review_id="review-001",
        interpretation="CONSISTENT",
    )

    assert (
        interpretation.interpretation
        == "CONSISTENT"
    )


def test_serializes():

    interpretation = ConstitutionalInterpretation(
        review_id="review-001",
        interpretation="CONSISTENT",
    )

    assert interpretation.to_dict() == {
        "review_id":
            "review-001",
        "interpretation":
            "CONSISTENT",
    }
