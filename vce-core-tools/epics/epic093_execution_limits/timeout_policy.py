from epics.epic093_execution_limits.execution_limits import (
    ExecutionLimits,
)


class TimeoutPolicy:

    @staticmethod
    def allow(
        elapsed_ms: int,
        limits: ExecutionLimits,
    ) -> bool:

        return elapsed_ms <= limits.timeout_ms
