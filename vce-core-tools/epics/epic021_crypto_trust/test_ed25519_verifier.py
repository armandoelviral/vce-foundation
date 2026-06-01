from epics.epic021_crypto_trust.ed25519_signer import (
    Ed25519Signer
)

from epics.epic021_crypto_trust.ed25519_verifier import (
    Ed25519Verifier
)


signer = Ed25519Signer()
verifier = Ed25519Verifier()

keys = signer.generate_keypair()

payload = b"artifact-001"

signature = signer.sign(
    keys["private_key"],
    payload
)


print(
    verifier.verify(
        keys["public_key"],
        payload,
        signature
    )
)


print(
    verifier.verify(
        keys["public_key"],
        b"tampered-artifact",
        signature
    )
)
