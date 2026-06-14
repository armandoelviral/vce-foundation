from epics.epic097_native_ed25519_signatures.ed25519_key_pair import (
    Ed25519KeyPair,
)


def test_generates_ed25519_key_pair():

    pair = Ed25519KeyPair.generate()

    assert pair.private_key is not None
    assert pair.public_key is not None


def test_exports_public_key_bytes():

    pair = Ed25519KeyPair.generate()

    public_key_bytes = pair.public_key_bytes()

    assert isinstance(public_key_bytes, bytes)
    assert len(public_key_bytes) > 0
