from epics.epic095_signed_wasm_artifacts.wasm_artifact_identity import (
    WasmArtifactIdentity,
)

from epics.epic095_signed_wasm_artifacts.wasm_artifact_hash import (
    WasmArtifactHash,
)

from epics.epic095_signed_wasm_artifacts.wasm_artifact_signature import (
    WasmArtifactSignature,
)

from epics.epic095_signed_wasm_artifacts.trusted_wasm_admission_gate import (
    TrustedWasmAdmissionGate,
)


def test_end_to_end_trusted_wasm_flow():

    artifact = WasmArtifactIdentity(
        artifact_id="artifact-001",
        module_name="calculator.wasm",
    )

    artifact_hash = WasmArtifactHash.compute(
        artifact
    )

    signature = WasmArtifactSignature.sign(
        artifact_hash
    )

    trusted = TrustedWasmAdmissionGate.admit(
        artifact_hash,
        signature,
    )

    assert trusted is True
