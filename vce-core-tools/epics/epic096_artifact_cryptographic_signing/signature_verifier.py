from epics.epic096_artifact_cryptographic_signing.artifact_signer import (
    ArtifactSigner,
)


class SignatureVerifier:

    @staticmethod
    def verify(
        artifact_hash: str,
        signature: str,
        private_key: str,
    ) -> bool:

        expected = ArtifactSigner.sign(
            artifact_hash=artifact_hash,
            private_key=private_key,
        )

        return signature == expected
