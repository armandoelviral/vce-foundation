from sp001.models.case import Case
from sp001.models.objective import Objective
from sp001.runtime.runtime_result import RuntimeResult
from sp001.runtime.transitions.objective_to_case import (
    ObjectiveToCaseTransition,
)


def test_objective_to_case_transition_returns_runtime_result() -> None:
    transition = ObjectiveToCaseTransition()
    objective = Objective(
        objective_id="OBJ-001",
        title="Increase pink dress sell-through",
        description="Improve sell-through before Back to School.",
    )

    result = transition.execute(
        objective,
        case_id="CASE-001",
        scope="STORE-MX-014",
    )

    assert isinstance(result, RuntimeResult)
    assert result.success is True
    assert result.transition == "Objective->Case"

    assert isinstance(result.output, Case)
    assert result.output.case_id == "CASE-001"
    assert result.output.objective_id == "OBJ-001"
    assert result.output.objective_title == objective.title
    assert result.output.scope == "STORE-MX-014"
