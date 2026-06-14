from epics.epic095_signed_wasm_artifacts.wasm_artifact_signature import (
    WasmArtifactSignature,
)

from epics.epic095_signed_wasm_artifacts.wasm_artifact_verifier import (
    WasmArtifactVerifier,
)


def test_verifier_accepts_valid_signature():

    artifact_hash = "artifact-hash-001"

    signature = WasmArtifactSignature.sign(
        artifact_hash
    )

    assert WasmArtifactVerifier.verify(
        artifact_hash,
        signature,
    )


def test_verifier_rejects_invalid_signature():

    assert not WasmArtifactVerifier.verify(
        "artifact-hash-001",
        "tampered-signature",
    )
