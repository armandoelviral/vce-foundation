from sp001.models.case import Case
from sp001.models.objective import Objective


class ScientificProductRuntime:
    """Coordinates Scientific Product lifecycle transitions."""

    def create_case(
        self,
        objective: Objective,
        *,
        case_id: str = "",
        scope: str = "",
    ) -> Case:
        return Case(
            case_id=case_id,
            objective_id=objective.objective_id,
            objective_title=objective.title,
            scope=scope,
        )
