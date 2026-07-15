from sp001.models.expert_decision import ExpertDecision
from sp001.models.recommendation import Recommendation
from sp001.runtime.runtime_result import RuntimeResult
from sp001.runtime.transitions.recommendation_to_expert_decision import (
    RecommendationToExpertDecisionTransition,
)


def test_recommendation_to_expert_decision_transition() -> None:
    transition = RecommendationToExpertDecisionTransition()

    recommendation = Recommendation()

    result = transition.execute(recommendation)

    assert isinstance(result, RuntimeResult)
    assert result.success
    assert result.transition == "Recommendation->ExpertDecision"
    assert isinstance(result.output, ExpertDecision)
