from epics.epic093_execution_limits.execution_limits import (
    ExecutionLimits,
)


class MemoryLimitPolicy:

    @staticmethod
    def allow(
        consumed_pages: int,
        limits: ExecutionLimits,
    ) -> bool:

        return consumed_pages <= limits.memory_pages
