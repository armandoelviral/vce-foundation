from epics.epic093_execution_limits.execution_limits import (
    ExecutionLimits,
)


class FuelBudgetPolicy:

    @staticmethod
    def allow(
        consumed_fuel: int,
        limits: ExecutionLimits,
    ) -> bool:

        return consumed_fuel <= limits.fuel
