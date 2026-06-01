from epics.epic021_crypto_trust.ed25519_signer import (
    Ed25519Signer
)


crypto = Ed25519Signer()

keys = crypto.generate_keypair()

signature = crypto.sign(
    keys["private_key"],
    b"artifact-001"
)


print(
    len(signature) > 0
)
