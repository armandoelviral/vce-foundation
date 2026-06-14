from epics.epic095_signed_wasm_artifacts.wasm_artifact_hash import (
    WasmArtifactHash,
)

from epics.epic095_signed_wasm_artifacts.wasm_artifact_identity import (
    WasmArtifactIdentity,
)


def test_hash_is_deterministic():

    artifact = WasmArtifactIdentity(
        artifact_id="artifact-001",
        module_name="calculator.wasm",
    )

    hash_1 = WasmArtifactHash.compute(
        artifact
    )

    hash_2 = WasmArtifactHash.compute(
        artifact
    )

    assert hash_1 == hash_2


def test_hash_changes_when_artifact_changes():

    artifact_a = WasmArtifactIdentity(
        artifact_id="artifact-001",
        module_name="calculator.wasm",
    )

    artifact_b = WasmArtifactIdentity(
        artifact_id="artifact-002",
        module_name="calculator.wasm",
    )

    assert (
        WasmArtifactHash.compute(
            artifact_a
        )
        !=
        WasmArtifactHash.compute(
            artifact_b
        )
    )
