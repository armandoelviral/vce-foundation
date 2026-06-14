def test_cryptography_ed25519_available():

    from cryptography.hazmat.primitives.asymmetric import ed25519

    assert ed25519.Ed25519PrivateKey is not None
    assert ed25519.Ed25519PublicKey is not None
