from __future__ import annotations

from dataclasses import dataclass

from has.conformance.model.decision import Decision
from has.conformance.model.evidence import Evidence


@dataclass(frozen=True, slots=True)
class DecisionRecord:
    """
    Immutable result produced by conformance evaluation.
    """

    claim: str
    capability: str
    executable_contract: str
    coverage_status: str
    decision: Decision
    evidence: Evidence
    failure_reason: str | None = None

    def __post_init__(self) -> None:
        if self.decision.is_conformant:
            if self.failure_reason is not None:
                raise ValueError(
                    "conformant decision cannot contain "
                    "a failure reason"
                )

            if not self.evidence.available:
                raise ValueError(
                    "conformant decision requires "
                    "available evidence"
                )

            if self.coverage_status != "Covered":
                raise ValueError(
                    "conformant decision requires "
                    "covered status"
                )

    @property
    def conformant(self) -> bool:
        return self.decision.is_conformant
