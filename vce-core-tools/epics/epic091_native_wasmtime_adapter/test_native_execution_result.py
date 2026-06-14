from epics.epic091_native_wasmtime_adapter.native_execution_result import (
    NativeExecutionResult,
)


def test_native_execution_result_contains_status():

    result = NativeExecutionResult(
        module_hash="module-001",
        function_name="run",
        output_payload={"value": 42},
        success=True,
        trap=None,
    )

    assert result.module_hash == "module-001"
    assert result.function_name == "run"
    assert result.output_payload == {"value": 42}
    assert result.success is True
    assert result.trap is None


def test_native_execution_result_serializes():

    result = NativeExecutionResult(
        module_hash="module-001",
        function_name="run",
        output_payload={"value": 42},
        success=True,
        trap=None,
    )

    assert result.to_dict() == {
        "module_hash": "module-001",
        "function_name": "run",
        "output_payload": {"value": 42},
        "success": True,
        "trap": None,
    }
