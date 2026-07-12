from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Recommendation:
    """Represents a proposed organizational action."""
