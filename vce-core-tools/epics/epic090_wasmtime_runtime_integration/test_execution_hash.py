from epics.epic090_wasmtime_runtime_integration.execution_hash import (
    ExecutionHash,
)

from epics.epic090_wasmtime_runtime_integration.wasmtime_runtime_contract import (
    WasmtimeExecutionResult,
)


def test_execution_hash_is_deterministic():

    result = WasmtimeExecutionResult(
        module_hash="module-001",
        function_name="run",
        output_payload={"value": 42},
        success=True,
    )

    hash1 = ExecutionHash.compute(result)
    hash2 = ExecutionHash.compute(result)

    assert hash1 == hash2


def test_execution_hash_changes_when_output_changes():

    result_a = WasmtimeExecutionResult(
        module_hash="module-001",
        function_name="run",
        output_payload={"value": 42},
        success=True,
    )

    result_b = WasmtimeExecutionResult(
        module_hash="module-001",
        function_name="run",
        output_payload={"value": 43},
        success=True,
    )

    assert (
        ExecutionHash.compute(result_a)
        != ExecutionHash.compute(result_b)
    )
