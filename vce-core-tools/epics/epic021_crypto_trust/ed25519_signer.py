from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)


class Ed25519Signer:

    def generate_keypair(self):

        private_key = (
            Ed25519PrivateKey.generate()
        )

        public_key = (
            private_key.public_key()
        )

        return {
            "private_key": private_key,
            "public_key": public_key,
        }


    def sign(
        self,
        private_key,
        payload: bytes,
    ):

        return private_key.sign(
            payload
        )
