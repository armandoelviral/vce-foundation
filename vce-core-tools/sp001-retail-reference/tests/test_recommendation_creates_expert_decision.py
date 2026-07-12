from sp001.models.recommendation import Recommendation
from sp001.models.expert_decision import ExpertDecision


def test_recommendation_creates_expert_decision() -> None:
    recommendation = Recommendation()

    decision = recommendation.create_expert_decision()

    assert isinstance(decision, ExpertDecision)
