from __future__ import annotations

from .execution_result import ExecutionResult
from .execution_unit import ExecutionUnit
from .specification import Specification


class SpecificationRuntime:
    """
    Minimal Specification Runtime.

    Executes one Specification by evaluating
    every Execution Unit.
    """

    def execute(
        self,
        specification: Specification,
    ) -> ExecutionResult:

        evidence: list[str] = []

        decision = "PASS"

        for claim in specification.claims:

            unit = ExecutionUnit(
                claim=claim,
                contract=claim.contract,
            )

            claim_evidence, claim_decision = (
                unit.execute()
            )

            evidence.append(
                claim_evidence
            )

            if claim_decision != "PASS":
                decision = "FAIL"

        return ExecutionResult(
            specification_identifier=(
                specification.identifier
            ),
            passed=(
                decision == "PASS"
            ),
            evidence=tuple(evidence),
            decision=decision,
        )
