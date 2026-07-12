from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OperationalEvidence:
    """Represents an observed operational result."""
