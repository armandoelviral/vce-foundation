from cryptography.exceptions import InvalidSignature


class Ed25519Verifier:

    def verify(
        self,
        public_key,
        payload: bytes,
        signature: bytes,
    ):

        try:

            public_key.verify(
                signature,
                payload
            )

            return True

        except InvalidSignature:

            return False
