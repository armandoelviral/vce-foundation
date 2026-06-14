import hashlib


class WasmArtifactSignature:

    @staticmethod
    def sign(
        artifact_hash: str,
    ) -> str:

        return hashlib.sha256(
            artifact_hash.encode()
        ).hexdigest()
