from epics.epic090_wasmtime_runtime_integration.wasmtime_runtime_contract import (
    WasmtimeExecutionRequest,
    WasmtimeExecutionResult,
)


def test_execution_request_contains_module_identity():
    request = WasmtimeExecutionRequest(
        module_hash="module-abc123",
        function_name="run",
        input_payload={"value": 42},
    )

    assert request.module_hash == "module-abc123"
    assert request.function_name == "run"
    assert request.input_payload == {"value": 42}


def test_execution_result_contains_deterministic_output():
    result = WasmtimeExecutionResult(
        module_hash="module-abc123",
        function_name="run",
        output_payload={"result": 84},
        success=True,
    )

    assert result.module_hash == "module-abc123"
    assert result.function_name == "run"
    assert result.output_payload == {"result": 84}
    assert result.success is True
