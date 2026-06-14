from epics.ztc22_wasmtime_runtime_hardening.fuel_policy import (
    FuelPolicy,
)


def test_accepts_execution_within_budget():

    policy = FuelPolicy(
        max_fuel=1000,
    )

    assert policy.allow(
        consumed_fuel=500,
    )


def test_rejects_execution_over_budget():

    policy = FuelPolicy(
        max_fuel=1000,
    )

    assert not policy.allow(
        consumed_fuel=1500,
    )


def test_accepts_exact_budget():

    policy = FuelPolicy(
        max_fuel=1000,
    )

    assert policy.allow(
        consumed_fuel=1000,
    )
