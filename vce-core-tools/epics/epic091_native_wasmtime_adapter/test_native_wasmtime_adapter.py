from epics.epic091_native_wasmtime_adapter.native_wasmtime_adapter import (
    NativeWasmtimeAdapter,
)

from epics.epic090_wasmtime_runtime_integration.wasmtime_runtime_contract import (
    WasmtimeExecutionRequest,
)


def test_native_adapter_executes_request():

    adapter = NativeWasmtimeAdapter()

    request = WasmtimeExecutionRequest(
        module_hash="module-001",
        function_name="run",
        input_payload={"value": 42},
    )

    result = adapter.execute(request)

    assert result.module_hash == "module-001"
    assert result.function_name == "run"
    assert result.success is True


def test_native_adapter_returns_deterministic_payload():

    adapter = NativeWasmtimeAdapter()

    request = WasmtimeExecutionRequest(
        module_hash="module-001",
        function_name="run",
        input_payload={"value": 42},
    )

    result_1 = adapter.execute(request)
    result_2 = adapter.execute(request)

    assert result_1.output_payload == result_2.output_payload
