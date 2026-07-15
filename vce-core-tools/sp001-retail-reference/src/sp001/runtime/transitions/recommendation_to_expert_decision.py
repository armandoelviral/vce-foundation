from sp001.models.expert_decision import ExpertDecision
from sp001.models.recommendation import Recommendation
from sp001.runtime.runtime_result import RuntimeResult


class RecommendationToExpertDecisionTransition:
    """Executes the transition from Recommendation to ExpertDecision."""

    transition_name = "Recommendation->ExpertDecision"

    def execute(
        self,
        recommendation: Recommendation,
    ) -> RuntimeResult:
        decision = ExpertDecision()

        return RuntimeResult(
            output=decision,
            transition=self.transition_name,
            success=True,
        )
