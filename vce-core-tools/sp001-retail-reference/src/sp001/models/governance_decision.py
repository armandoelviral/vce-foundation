from dataclasses import dataclass

from .institutional_capability import InstitutionalCapability


@dataclass(frozen=True, slots=True)
class GovernanceDecision:
    """Represents the formal governance outcome for a capability candidate."""

    def create_institutional_capability(self) -> InstitutionalCapability:
        return InstitutionalCapability()
