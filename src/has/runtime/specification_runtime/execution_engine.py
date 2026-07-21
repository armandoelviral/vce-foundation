from __future__ import annotations

from .execution_unit import ExecutionUnit


class ExecutionEngine:
    """
    Execute Runtime Execution Units.
    """

    def execute(
        self,
        units: tuple[ExecutionUnit, ...],
    ) -> tuple[tuple[str, str], ...]:

        return tuple(
            unit.execute()
            for unit in units
        )
