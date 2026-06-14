import hashlib


class ArtifactHashBinding:

    @staticmethod
    def compute(
        artifact_hash: str,
        execution_id: str,
    ) -> str:

        payload = (
            f"{artifact_hash}:{execution_id}"
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()
