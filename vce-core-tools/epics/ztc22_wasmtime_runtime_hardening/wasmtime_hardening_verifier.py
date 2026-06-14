from epics.ztc22_wasmtime_runtime_hardening.wasmtime_execution_profile import (
    WasmtimeExecutionProfile,
)


class WasmtimeHardeningVerifier:

    def verify(
        self,
        profile: WasmtimeExecutionProfile,
    ) -> bool:

        if profile.max_fuel <= 0:
            return False

        if profile.max_memory_bytes <= 0:
            return False

        if not profile.deterministic_required:
            return False

        return True
