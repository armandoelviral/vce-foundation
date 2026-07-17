from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConformanceInput:
    """
    Immutable input consumed by the
    Conformance Evaluator.
    """

    claim: str

    capability: str

    executable_contract: str

    coverage_status: str

    def is_covered(self) -> bool:
        return self.coverage_status == "Covered"
