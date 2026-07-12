from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExpertDecision:
    """Represents explicit human judgment."""
