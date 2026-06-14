from epics.epic093_execution_limits.execution_limits import (
    ExecutionLimits,
)

from epics.epic093_execution_limits.timeout_policy import (
    TimeoutPolicy,
)


def test_accepts_execution_within_timeout():

    limits = ExecutionLimits(
        fuel=100,
        timeout_ms=1000,
        memory_pages=16,
    )

    assert TimeoutPolicy.allow(
        elapsed_ms=500,
        limits=limits,
    )


def test_accepts_execution_at_timeout_boundary():

    limits = ExecutionLimits(
        fuel=100,
        timeout_ms=1000,
        memory_pages=16,
    )

    assert TimeoutPolicy.allow(
        elapsed_ms=1000,
        limits=limits,
    )


def test_rejects_execution_over_timeout():

    limits = ExecutionLimits(
        fuel=100,
        timeout_ms=1000,
        memory_pages=16,
    )

    assert not TimeoutPolicy.allow(
        elapsed_ms=1001,
        limits=limits,
    )
