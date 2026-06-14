from epics.epic091_native_wasmtime_adapter.native_wasmtime_adapter import (
    NativeWasmtimeAdapter,
)

from epics.epic091_native_wasmtime_adapter.native_execution_verifier import (
    NativeExecutionVerifier,
)

from epics.epic090_wasmtime_runtime_integration.wasmtime_runtime_contract import (
    WasmtimeExecutionRequest,
)


def test_end_to_end_native_wasm_flow():

    adapter = NativeWasmtimeAdapter()

    request = WasmtimeExecutionRequest(
        module_hash="module-001",
        function_name="run",
        input_payload={"value": 42},
    )

    result_1 = adapter.execute(request)
    result_2 = adapter.execute(request)

    verified = NativeExecutionVerifier.verify(
        result_1,
        result_2,
    )

    assert verified is True
