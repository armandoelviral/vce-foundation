from epics.epic091_native_wasmtime_adapter.native_execution_result import (
    NativeExecutionResult,
)

from epics.epic091_native_wasmtime_adapter.native_execution_verifier import (
    NativeExecutionVerifier,
)


def test_accepts_equivalent_results():

    result_a = NativeExecutionResult(
        module_hash="module-001",
        function_name="run",
        output_payload={"value": 42},
        success=True,
        trap=None,
    )

    result_b = NativeExecutionResult(
        module_hash="module-001",
        function_name="run",
        output_payload={"value": 42},
        success=True,
        trap=None,
    )

    assert NativeExecutionVerifier.verify(
        result_a,
        result_b,
    )


def test_rejects_different_results():

    result_a = NativeExecutionResult(
        module_hash="module-001",
        function_name="run",
        output_payload={"value": 42},
        success=True,
        trap=None,
    )

    result_b = NativeExecutionResult(
        module_hash="module-001",
        function_name="run",
        output_payload={"value": 99},
        success=True,
        trap=None,
    )

    assert not NativeExecutionVerifier.verify(
        result_a,
        result_b,
    )
