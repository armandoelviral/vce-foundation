from epics.ztc22_wasmtime_runtime_hardening.wasmtime_module_guard import (
    WasmtimeModuleGuard,
)

from epics.ztc22_wasmtime_runtime_hardening.fuel_policy import (
    FuelPolicy,
)

from epics.ztc22_wasmtime_runtime_hardening.memory_limit_policy import (
    MemoryLimitPolicy,
)

from epics.ztc22_wasmtime_runtime_hardening.import_restriction_policy import (
    ImportRestrictionPolicy,
)

from epics.ztc22_wasmtime_runtime_hardening.deterministic_execution_policy import (
    DeterministicExecutionPolicy,
)

from epics.ztc22_wasmtime_runtime_hardening.wasmtime_execution_profile import (
    WasmtimeExecutionProfile,
)

from epics.ztc22_wasmtime_runtime_hardening.wasmtime_hardening_verifier import (
    WasmtimeHardeningVerifier,
)


def test_end_to_end_wasmtime_hardening_flow():

    assert WasmtimeModuleGuard.allow(
        module_name="policy.wasm",
        module_hash="hash-001",
    )

    fuel_policy = FuelPolicy(
        max_fuel=1000,
    )

    assert fuel_policy.allow(
        consumed_fuel=500,
    )

    memory_policy = MemoryLimitPolicy(
        max_memory_bytes=65536,
    )

    assert memory_policy.allow(
        requested_memory_bytes=32768,
    )

    import_policy = ImportRestrictionPolicy(
        allowed_imports={
            "env.log",
        }
    )

    assert import_policy.allow(
        "env.log"
    )

    deterministic_policy = DeterministicExecutionPolicy()

    assert deterministic_policy.allow(
        uses_system_time=False,
        uses_randomness=False,
    )

    profile = WasmtimeExecutionProfile(
        max_fuel=1000,
        max_memory_bytes=65536,
        allowed_imports={
            "env.log",
        },
        deterministic_required=True,
    )

    verifier = WasmtimeHardeningVerifier()

    assert verifier.verify(
        profile
    )
