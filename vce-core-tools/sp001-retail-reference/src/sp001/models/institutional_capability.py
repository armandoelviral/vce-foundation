from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InstitutionalCapability:
    """Represents a governed permanent organizational capability."""
