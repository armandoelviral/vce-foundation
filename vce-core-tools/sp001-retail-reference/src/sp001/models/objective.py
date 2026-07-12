from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Objective:
    """Represents organizational intent."""
