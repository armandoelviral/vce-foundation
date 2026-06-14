from epics.epic095_signed_wasm_artifacts.wasm_artifact_identity import (
    WasmArtifactIdentity,
)


def test_artifact_identity_contains_module_reference():

    artifact = WasmArtifactIdentity(
        artifact_id="artifact-001",
        module_name="calculator.wasm",
    )

    assert artifact.artifact_id == "artifact-001"
    assert artifact.module_name == "calculator.wasm"


def test_artifact_identity_serializes():

    artifact = WasmArtifactIdentity(
        artifact_id="artifact-001",
        module_name="calculator.wasm",
    )

    assert artifact.to_dict() == {
        "artifact_id": "artifact-001",
        "module_name": "calculator.wasm",
    }
