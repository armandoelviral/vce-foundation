from epics.epic093_execution_limits.execution_limits import (
    ExecutionLimits,
)

from epics.epic093_execution_limits.memory_limit_policy import (
    MemoryLimitPolicy,
)


def test_accepts_memory_within_limit():

    limits = ExecutionLimits(
        fuel=100,
        timeout_ms=1000,
        memory_pages=16,
    )

    assert MemoryLimitPolicy.allow(
        consumed_pages=8,
        limits=limits,
    )


def test_accepts_memory_at_boundary():

    limits = ExecutionLimits(
        fuel=100,
        timeout_ms=1000,
        memory_pages=16,
    )

    assert MemoryLimitPolicy.allow(
        consumed_pages=16,
        limits=limits,
    )


def test_rejects_memory_over_limit():

    limits = ExecutionLimits(
        fuel=100,
        timeout_ms=1000,
        memory_pages=16,
    )

    assert not MemoryLimitPolicy.allow(
        consumed_pages=17,
        limits=limits,
    )
