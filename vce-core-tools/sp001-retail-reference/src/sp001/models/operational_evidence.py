from dataclasses import dataclass

from .capability_candidate import CapabilityCandidate


@dataclass(frozen=True, slots=True)
class OperationalEvidence:
    """Represents an observed operational result."""

    def create_capability_candidate(self) -> CapabilityCandidate:
        return CapabilityCandidate()
