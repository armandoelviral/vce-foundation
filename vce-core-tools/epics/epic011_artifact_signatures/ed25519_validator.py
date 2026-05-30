from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

private_key = ed25519.Ed25519PrivateKey.generate()
public_key = private_key.public_key()

original_payload = b"VCE Artifact Payload"

signature = private_key.sign(original_payload)

tampered_payload = b"VCE Artifact Payload TAMPERED"

try:
    public_key.verify(
        signature,
        tampered_payload
    )

    print("VALID")

except InvalidSignature:

    print("INVALID")
