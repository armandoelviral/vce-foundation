from epics.epic090_wasmtime_runtime_integration.deterministic_execution_verifier import (
    DeterministicExecutionVerifier,
)

from epics.epic090_wasmtime_runtime_integration.wasmtime_execution_adapter import (
    WasmtimeExecutionAdapter,
)

from epics.epic090_wasmtime_runtime_integration.wasmtime_runtime_contract import (
    WasmtimeExecutionRequest,
)


def test_verifier_accepts_deterministic_execution():
    adapter = WasmtimeExecutionAdapter()

    request = WasmtimeExecutionRequest(
        module_hash="module-001",
        function_name="run",
        input_payload={"value": 42},
    )

    result_1 = adapter.execute(request)
    result_2 = adapter.execute(request)

    assert DeterministicExecutionVerifier.verify(
        result_1,
        result_2,
    )


def test_verifier_rejects_different_outputs():
    adapter = WasmtimeExecutionAdapter()

    request_a = WasmtimeExecutionRequest(
        module_hash="module-001",
        function_name="run",
        input_payload={"value": 42},
    )

    request_b = WasmtimeExecutionRequest(
        module_hash="module-001",
        function_name="run",
        input_payload={"value": 43},
    )

    result_1 = adapter.execute(request_a)
    result_2 = adapter.execute(request_b)

    assert not DeterministicExecutionVerifier.verify(
        result_1,
        result_2,
    )
