from epics.ztc22_wasmtime_runtime_hardening.wasmtime_execution_profile import (
    WasmtimeExecutionProfile,
)

from epics.ztc22_wasmtime_runtime_hardening.wasmtime_hardening_verifier import (
    WasmtimeHardeningVerifier,
)


def test_accepts_hardened_profile():

    profile = WasmtimeExecutionProfile(
        max_fuel=1000,
        max_memory_bytes=65536,
        allowed_imports={"env.log"},
        deterministic_required=True,
    )

    verifier = WasmtimeHardeningVerifier()

    assert verifier.verify(profile)


def test_rejects_zero_fuel_budget():

    profile = WasmtimeExecutionProfile(
        max_fuel=0,
        max_memory_bytes=65536,
        allowed_imports={"env.log"},
        deterministic_required=True,
    )

    verifier = WasmtimeHardeningVerifier()

    assert not verifier.verify(profile)


def test_rejects_zero_memory_limit():

    profile = WasmtimeExecutionProfile(
        max_fuel=1000,
        max_memory_bytes=0,
        allowed_imports={"env.log"},
        deterministic_required=True,
    )

    verifier = WasmtimeHardeningVerifier()

    assert not verifier.verify(profile)


def test_rejects_non_deterministic_profile():

    profile = WasmtimeExecutionProfile(
        max_fuel=1000,
        max_memory_bytes=65536,
        allowed_imports={"env.log"},
        deterministic_required=False,
    )

    verifier = WasmtimeHardeningVerifier()

    assert not verifier.verify(profile)
