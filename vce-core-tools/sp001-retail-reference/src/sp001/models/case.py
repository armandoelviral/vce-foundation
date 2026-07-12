from dataclasses import dataclass

from .recommendation import Recommendation


@dataclass(frozen=True, slots=True)
class Case:
    """Represents a concrete execution pursuing an objective."""

    def create_recommendation(self) -> Recommendation:
        return Recommendation()
