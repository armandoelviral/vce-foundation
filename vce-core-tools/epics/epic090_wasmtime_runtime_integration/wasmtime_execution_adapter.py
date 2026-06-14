from epics.epic090_wasmtime_runtime_integration.wasmtime_runtime_contract import (
    WasmtimeExecutionRequest,
    WasmtimeExecutionResult,
)


class WasmtimeExecutionAdapter:

    def execute(
        self,
        request: WasmtimeExecutionRequest,
    ) -> WasmtimeExecutionResult:

        return WasmtimeExecutionResult(
            module_hash=request.module_hash,
            function_name=request.function_name,
            output_payload=request.input_payload,
            success=True,
        )
