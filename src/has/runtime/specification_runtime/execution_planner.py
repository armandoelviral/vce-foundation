from __future__ import annotations

from .execution_unit import ExecutionUnit
from .specification import Specification


class ExecutionPlanner:
    """
    Transform one Specification into
    executable Execution Units.
    """

    def plan(
        self,
        specification: Specification,
    ) -> tuple[ExecutionUnit, ...]:

        return tuple(
            ExecutionUnit(
                claim=claim,
                contract=claim.contract,
            )
            for claim in specification.claims
        )
