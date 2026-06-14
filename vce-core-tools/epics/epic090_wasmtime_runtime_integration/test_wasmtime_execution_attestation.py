from epics.epic090_wasmtime_runtime_integration.wasmtime_execution_attestation import (
    WasmtimeExecutionAttestation,
)


def test_attestation_contains_execution_identity():

    attestation = WasmtimeExecutionAttestation(
        module_hash="module-001",
        function_name="run",
        execution_hash="exec-123",
        verified=True,
    )

    assert attestation.module_hash == "module-001"
    assert attestation.function_name == "run"
    assert attestation.execution_hash == "exec-123"
    assert attestation.verified is True


def test_attestation_serializes():

    attestation = WasmtimeExecutionAttestation(
        module_hash="module-001",
        function_name="run",
        execution_hash="exec-123",
        verified=True,
    )

    assert attestation.to_dict() == {
        "module_hash": "module-001",
        "function_name": "run",
        "execution_hash": "exec-123",
        "verified": True,
    }
