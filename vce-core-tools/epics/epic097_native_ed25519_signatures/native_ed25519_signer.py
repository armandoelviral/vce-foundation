from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)


class NativeEd25519Signer:

    @staticmethod
    def sign(
        artifact_hash: str,
        private_key: Ed25519PrivateKey,
    ) -> bytes:

        return private_key.sign(
            artifact_hash.encode()
        )
