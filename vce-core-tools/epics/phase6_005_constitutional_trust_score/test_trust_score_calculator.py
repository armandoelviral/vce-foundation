from epics.phase6_005_constitutional_trust_score.trust_score_calculator import (
    calculate_constitutional_trust_score,
)


def test_calculates_trust_score():
    score = calculate_constitutional_trust_score(
        reputation_score=80,
        credibility_score=70,
        trust_score=90,
    )

    assert score == 80
