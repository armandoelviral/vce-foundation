from epics.epic090_wasmtime_runtime_integration.wasmtime_runtime_contract import (
    WasmtimeExecutionResult,
)


class DeterministicExecutionVerifier:

    @staticmethod
    def verify(
        first: WasmtimeExecutionResult,
        second: WasmtimeExecutionResult,
    ) -> bool:

        return (
            first.module_hash == second.module_hash
            and first.function_name == second.function_name
            and first.output_payload == second.output_payload
            and first.success == second.success
        )
