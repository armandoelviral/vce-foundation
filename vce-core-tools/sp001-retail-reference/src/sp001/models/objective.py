from dataclasses import dataclass

from .case import Case


@dataclass(frozen=True, slots=True)
class Objective:
    """Represents explicit organizational intent."""

    objective_id: str = ""
    title: str = ""
    description: str = ""

    def create_case(self, case_id: str = "", scope: str = "") -> Case:
        return Case(
            case_id=case_id,
            objective_id=self.objective_id,
            objective_title=self.title,
            scope=scope,
        )
