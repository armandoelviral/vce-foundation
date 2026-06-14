from epics.epic093_execution_limits.execution_limits import (
    ExecutionLimits,
)

from epics.epic093_execution_limits.execution_safety_gate import (
    ExecutionSafetyGate,
)


def test_accepts_safe_execution():

    limits = ExecutionLimits(
        fuel=100,
        timeout_ms=1000,
        memory_pages=16,
    )

    assert ExecutionSafetyGate.allow(
        consumed_fuel=50,
        elapsed_ms=500,
        consumed_pages=8,
        limits=limits,
    )


def test_rejects_fuel_violation():

    limits = ExecutionLimits(
        fuel=100,
        timeout_ms=1000,
        memory_pages=16,
    )

    assert not ExecutionSafetyGate.allow(
        consumed_fuel=101,
        elapsed_ms=500,
        consumed_pages=8,
        limits=limits,
    )


def test_rejects_timeout_violation():

    limits = ExecutionLimits(
        fuel=100,
        timeout_ms=1000,
        memory_pages=16,
    )

    assert not ExecutionSafetyGate.allow(
        consumed_fuel=50,
        elapsed_ms=1001,
        consumed_pages=8,
        limits=limits,
    )


def test_rejects_memory_violation():

    limits = ExecutionLimits(
        fuel=100,
        timeout_ms=1000,
        memory_pages=16,
    )

    assert not ExecutionSafetyGate.allow(
        consumed_fuel=50,
        elapsed_ms=500,
        consumed_pages=17,
        limits=limits,
    )
