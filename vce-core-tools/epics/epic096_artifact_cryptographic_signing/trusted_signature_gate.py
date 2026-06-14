from epics.epic096_artifact_cryptographic_signing.signature_verifier import (
    SignatureVerifier,
)

from epics.epic096_artifact_cryptographic_signing.signed_artifact import (
    SignedArtifact,
)


class TrustedSignatureGate:

    @staticmethod
    def admit(
        signed_artifact: SignedArtifact,
        private_key: str,
    ) -> bool:

        return SignatureVerifier.verify(
            artifact_hash=signed_artifact.artifact_hash,
            signature=signed_artifact.signature,
            private_key=private_key,
        )
