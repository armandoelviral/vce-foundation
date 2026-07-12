from dataclasses import dataclass

from .recommendation import Recommendation


@dataclass(frozen=True, slots=True)
class Case:
    """Represents a concrete execution pursuing an objective."""

    case_id: str = ""
    objective_id: str = ""
    objective_title: str = ""
    scope: str = ""

    def create_recommendation(self) -> Recommendation:
        return Recommendation()
