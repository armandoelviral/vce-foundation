from epics.epic095_signed_wasm_artifacts.wasm_artifact_signature import (
    WasmArtifactSignature,
)


class WasmArtifactVerifier:

    @staticmethod
    def verify(
        artifact_hash: str,
        signature: str,
    ) -> bool:

        expected_signature = (
            WasmArtifactSignature.sign(
                artifact_hash
            )
        )

        return signature == expected_signature
