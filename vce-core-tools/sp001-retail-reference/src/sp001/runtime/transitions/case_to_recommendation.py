from sp001.models.case import Case
from sp001.models.recommendation import Recommendation
from sp001.runtime.runtime_result import RuntimeResult


class CaseToRecommendationTransition:
    """Executes the transition from Case to Recommendation."""

    transition_name = "Case->Recommendation"

    def execute(self, case: Case) -> RuntimeResult:
        recommendation = Recommendation()

        return RuntimeResult(
            output=recommendation,
            transition=self.transition_name,
            success=True,
        )
