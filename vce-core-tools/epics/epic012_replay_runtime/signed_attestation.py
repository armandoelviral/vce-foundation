import json

from cryptography.hazmat.primitives.asymmetric import ed25519


class SignedAttestation:

    def __init__(self):

        self.private_key = (
            ed25519.Ed25519PrivateKey.generate()
        )

        self.public_key = (
            self.private_key.public_key()
        )


    def sign(self, attestation):

        payload = json.dumps(
            attestation,
            sort_keys=True
        ).encode()

        signature = (
            self.private_key.sign(payload)
        )

        return {
            "attestation": attestation,
            "signature": signature.hex()
        }


    def verify(self, signed):

        payload = json.dumps(
            signed["attestation"],
            sort_keys=True
        ).encode()

        signature = bytes.fromhex(
            signed["signature"]
        )

        self.public_key.verify(
            signature,
            payload
        )

        return True
