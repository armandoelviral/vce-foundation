from dataclasses import dataclass

from .expert_decision import ExpertDecision


@dataclass(frozen=True, slots=True)
class Recommendation:
    """Represents a proposed organizational action."""

    def create_expert_decision(self) -> ExpertDecision:
        return ExpertDecision()
