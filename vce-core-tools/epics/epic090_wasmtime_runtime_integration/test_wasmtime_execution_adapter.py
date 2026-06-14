from epics.epic090_wasmtime_runtime_integration.wasmtime_execution_adapter import (
    WasmtimeExecutionAdapter,
)

from epics.epic090_wasmtime_runtime_integration.wasmtime_runtime_contract import (
    WasmtimeExecutionRequest,
)


def test_adapter_executes_request():

    adapter = WasmtimeExecutionAdapter()

    request = WasmtimeExecutionRequest(
        module_hash="module-001",
        function_name="run",
        input_payload={
            "value": 42,
        },
    )

    result = adapter.execute(
        request
    )

    assert result.module_hash == "module-001"
    assert result.function_name == "run"
    assert result.success is True


def test_adapter_returns_payload():

    adapter = WasmtimeExecutionAdapter()

    request = WasmtimeExecutionRequest(
        module_hash="module-001",
        function_name="run",
        input_payload={
            "value": 42,
        },
    )

    result = adapter.execute(
        request
    )

    assert result.output_payload == {
        "value": 42,
    }
