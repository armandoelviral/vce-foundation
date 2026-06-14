from epics.epic095_signed_wasm_artifacts.wasm_artifact_signature import (
    WasmArtifactSignature,
)


def test_signature_is_deterministic():

    signature_1 = WasmArtifactSignature.sign(
        "artifact-hash-001"
    )

    signature_2 = WasmArtifactSignature.sign(
        "artifact-hash-001"
    )

    assert signature_1 == signature_2


def test_signature_changes_when_hash_changes():

    signature_1 = WasmArtifactSignature.sign(
        "artifact-hash-001"
    )

    signature_2 = WasmArtifactSignature.sign(
        "artifact-hash-002"
    )

    assert signature_1 != signature_2
