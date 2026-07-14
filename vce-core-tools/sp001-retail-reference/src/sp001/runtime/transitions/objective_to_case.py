from sp001.models.case import Case
from sp001.models.objective import Objective
from sp001.runtime.runtime_result import RuntimeResult


class ObjectiveToCaseTransition:
    """Executes the governed transition from Objective to Case."""

    transition_name = "Objective->Case"

    def execute(
        self,
        objective: Objective,
        *,
        case_id: str = "",
        scope: str = "",
    ) -> RuntimeResult:
        case = Case(
            case_id=case_id,
            objective_id=objective.objective_id,
            objective_title=objective.title,
            scope=scope,
        )

        return RuntimeResult(
            output=case,
            transition=self.transition_name,
            success=True,
        )
