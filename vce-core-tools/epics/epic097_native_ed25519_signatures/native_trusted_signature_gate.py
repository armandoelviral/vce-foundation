from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PublicKey,
)

from epics.epic097_native_ed25519_signatures.native_ed25519_verifier import (
    NativeEd25519Verifier,
)


class NativeTrustedSignatureGate:

    @staticmethod
    def admit(
        artifact_hash: str,
        signature: bytes,
        public_key: Ed25519PublicKey,
    ) -> bool:

        return NativeEd25519Verifier.verify(
            artifact_hash=artifact_hash,
            signature=signature,
            public_key=public_key,
        )
