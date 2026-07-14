from sp001.models.case import Case
from sp001.models.recommendation import Recommendation
from sp001.runtime.runtime_result import RuntimeResult
from sp001.runtime.transitions.case_to_recommendation import (
    CaseToRecommendationTransition,
)


def test_case_to_recommendation_transition_returns_runtime_result() -> None:
    transition = CaseToRecommendationTransition()
    case = Case(
        case_id="CASE-001",
        objective_id="OBJ-001",
        objective_title="Increase pink dress sell-through",
        scope="STORE-MX-014",
    )

    result = transition.execute(case)

    assert isinstance(result, RuntimeResult)
    assert result.success is True
    assert result.transition == "Case->Recommendation"
    assert isinstance(result.output, Recommendation)
