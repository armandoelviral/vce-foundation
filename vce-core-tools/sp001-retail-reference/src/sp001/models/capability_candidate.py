from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CapabilityCandidate:
    """Represents a capability awaiting validation and governance."""
