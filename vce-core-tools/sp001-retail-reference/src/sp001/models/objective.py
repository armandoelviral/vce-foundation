from dataclasses import dataclass

from .case import Case


@dataclass(frozen=True, slots=True)
class Objective:

    def create_case(self) -> Case:
        return Case()
