from epics.epic090_wasmtime_runtime_integration.deterministic_execution_verifier import (
    DeterministicExecutionVerifier,
)

from epics.epic090_wasmtime_runtime_integration.execution_hash import (
    ExecutionHash,
)

from epics.epic090_wasmtime_runtime_integration.wasmtime_execution_adapter import (
    WasmtimeExecutionAdapter,
)

from epics.epic090_wasmtime_runtime_integration.wasmtime_execution_attestation import (
    WasmtimeExecutionAttestation,
)

from epics.epic090_wasmtime_runtime_integration.wasmtime_runtime_contract import (
    WasmtimeExecutionRequest,
)


def test_end_to_end_wasmtime_execution_flow():

    adapter = WasmtimeExecutionAdapter()

    request = WasmtimeExecutionRequest(
        module_hash="module-001",
        function_name="run",
        input_payload={"value": 42},
    )

    result_1 = adapter.execute(request)
    result_2 = adapter.execute(request)

    verified = DeterministicExecutionVerifier.verify(
        result_1,
        result_2,
    )

    execution_hash = ExecutionHash.compute(
        result_1
    )

    attestation = WasmtimeExecutionAttestation(
        module_hash=result_1.module_hash,
        function_name=result_1.function_name,
        execution_hash=execution_hash,
        verified=verified,
    )

    assert attestation.module_hash == "module-001"
    assert attestation.function_name == "run"
    assert attestation.verified is True
