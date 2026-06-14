import hashlib
import json

from epics.epic095_signed_wasm_artifacts.wasm_artifact_identity import (
    WasmArtifactIdentity,
)


class WasmArtifactHash:

    @staticmethod
    def compute(
        artifact: WasmArtifactIdentity,
    ) -> str:

        payload = json.dumps(
            artifact.to_dict(),
            sort_keys=True,
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()
