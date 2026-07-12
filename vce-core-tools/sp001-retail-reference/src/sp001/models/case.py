from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Case:
    """Represents a concrete execution pursuing an objective."""
