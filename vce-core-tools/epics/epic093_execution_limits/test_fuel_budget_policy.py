from epics.epic093_execution_limits.fuel_budget_policy import (
    FuelBudgetPolicy,
)

from epics.epic093_execution_limits.execution_limits import (
    ExecutionLimits,
)


def test_accepts_execution_within_budget():

    limits = ExecutionLimits(
        fuel=100,
        timeout_ms=1000,
        memory_pages=16,
    )

    assert FuelBudgetPolicy.allow(
        consumed_fuel=50,
        limits=limits,
    )


def test_accepts_execution_at_boundary():

    limits = ExecutionLimits(
        fuel=100,
        timeout_ms=1000,
        memory_pages=16,
    )

    assert FuelBudgetPolicy.allow(
        consumed_fuel=100,
        limits=limits,
    )


def test_rejects_execution_over_budget():

    limits = ExecutionLimits(
        fuel=100,
        timeout_ms=1000,
        memory_pages=16,
    )

    assert not FuelBudgetPolicy.allow(
        consumed_fuel=101,
        limits=limits,
    )
