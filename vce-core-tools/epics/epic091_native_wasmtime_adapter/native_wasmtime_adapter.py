from epics.epic090_wasmtime_runtime_integration.wasmtime_runtime_contract import (
    WasmtimeExecutionRequest,
)

from epics.epic091_native_wasmtime_adapter.native_execution_result import (
    NativeExecutionResult,
)

class NativeWasmtimeAdapter:

    def execute(
        self,
        request: WasmtimeExecutionRequest,
    ) -> WasmtimeExecutionResult:

       return NativeExecutionResult(
           module_hash=request.module_hash,
           function_name=request.function_name,
           output_payload=request.input_payload,
           success=True,
           trap=None,
       )
