import hashlib


class ArtifactSigner:

    @staticmethod
    def sign(
        artifact_hash: str,
        private_key: str,
    ) -> str:

        payload = f"{artifact_hash}:{private_key}"

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()
