from dataclasses import dataclass

from .governance_decision import GovernanceDecision


@dataclass(frozen=True, slots=True)
class CapabilityCandidate:
    """Represents a capability awaiting validation and governance."""

    def create_governance_decision(self) -> GovernanceDecision:
        return GovernanceDecision()
