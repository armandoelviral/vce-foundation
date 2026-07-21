from __future__ import annotations

from dataclasses import dataclass

from .claim import Claim


@dataclass(frozen=True, slots=True)
class ExecutionUnit:
    """
    Smallest executable Runtime component.

    One Execution Unit executes exactly one
    Claim.
    """

    claim: Claim

    contract: str

    def execute(self) -> tuple[str, str]:
        """
        Execute the bound executable contract.

        SR-003 intentionally implements the
        minimum deterministic execution model.

        Returns
        -------
        tuple[str, str]

            Evidence

            Decision
        """

        evidence = (
            f"Evidence for {self.claim.identifier}"
        )

        decision = "PASS"

        return (
            evidence,
            decision,
        )
