from epics.epic095_signed_wasm_artifacts.wasm_artifact_verifier import (
    WasmArtifactVerifier,
)


class TrustedWasmAdmissionGate:

    @staticmethod
    def admit(
        artifact_hash: str,
        signature: str,
    ) -> bool:

        return WasmArtifactVerifier.verify(
            artifact_hash,
            signature,
        )
