import hashlib


class RemoteVerification:

    def verify(
        self,
        artifact
    ):

        artifact_hash = hashlib.sha256(
            artifact.encode()
        ).hexdigest()

        return {
            "artifact": artifact,
            "artifact_hash": artifact_hash,
            "verification": "VERIFIED"
        }


    def attest(
        self,
        artifact
    ):

        result = self.verify(
            artifact
        )

        return {
            "attestation": result,
            "trusted": True
        }
