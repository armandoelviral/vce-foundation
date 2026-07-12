from dataclasses import dataclass

from .operational_evidence import OperationalEvidence


@dataclass(frozen=True, slots=True)
class ExpertDecision:
    """Represents explicit human judgment."""

    def create_operational_evidence(self) -> OperationalEvidence:
        return OperationalEvidence()
