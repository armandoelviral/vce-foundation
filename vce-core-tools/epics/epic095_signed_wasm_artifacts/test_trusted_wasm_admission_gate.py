from epics.epic095_signed_wasm_artifacts.trusted_wasm_admission_gate import (
    TrustedWasmAdmissionGate,
)

from epics.epic095_signed_wasm_artifacts.wasm_artifact_signature import (
    WasmArtifactSignature,
)


def test_admits_valid_signed_artifact():

    artifact_hash = "artifact-hash-001"

    signature = WasmArtifactSignature.sign(
        artifact_hash
    )

    assert TrustedWasmAdmissionGate.admit(
        artifact_hash,
        signature,
    )


def test_rejects_invalid_signed_artifact():

    assert not TrustedWasmAdmissionGate.admit(
        "artifact-hash-001",
        "tampered-signature",
    )
