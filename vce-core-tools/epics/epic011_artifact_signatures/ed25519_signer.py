from cryptography.hazmat.primitives.asymmetric import ed25519


private_key = ed25519.Ed25519PrivateKey.generate()
public_key = private_key.public_key()

message = b"VCE Artifact Payload"

signature = private_key.sign(message)

print("MESSAGE:", message)
print("SIGNATURE:", signature.hex())

