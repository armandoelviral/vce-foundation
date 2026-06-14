from epics.epic093_execution_limits.fuel_budget_policy import (
    FuelBudgetPolicy,
)

from epics.epic093_execution_limits.timeout_policy import (
    TimeoutPolicy,
)

from epics.epic093_execution_limits.memory_limit_policy import (
    MemoryLimitPolicy,
)

from epics.epic093_execution_limits.execution_limits import (
    ExecutionLimits,
)


class ExecutionSafetyGate:

    @staticmethod
    def allow(
        consumed_fuel: int,
        elapsed_ms: int,
        consumed_pages: int,
        limits: ExecutionLimits,
    ) -> bool:

        return (
            FuelBudgetPolicy.allow(
                consumed_fuel,
                limits,
            )
            and TimeoutPolicy.allow(
                elapsed_ms,
                limits,
            )
            and MemoryLimitPolicy.allow(
                consumed_pages,
                limits,
            )
        )
