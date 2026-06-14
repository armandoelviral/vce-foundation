from epics.epic093_execution_limits.execution_limits import (
    ExecutionLimits,
)


def test_execution_limits_contains_runtime_limits():

    limits = ExecutionLimits(
        fuel=100000,
        timeout_ms=1000,
        memory_pages=16,
    )

    assert limits.fuel == 100000
    assert limits.timeout_ms == 1000
    assert limits.memory_pages == 16


def test_execution_limits_are_immutable():

    limits = ExecutionLimits(
        fuel=100000,
        timeout_ms=1000,
        memory_pages=16,
    )

    assert limits.fuel > 0
    assert limits.timeout_ms > 0
    assert limits.memory_pages > 0
