from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PublicKey,
)


class NativeEd25519Verifier:

    @staticmethod
    def verify(
        artifact_hash: str,
        signature: bytes,
        public_key: Ed25519PublicKey,
    ) -> bool:

        try:
            public_key.verify(
                signature,
                artifact_hash.encode(),
            )
            return True

        except InvalidSignature:
            return False
