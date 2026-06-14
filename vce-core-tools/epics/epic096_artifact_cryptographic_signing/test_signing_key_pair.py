from epics.epic096_artifact_cryptographic_signing.signing_key_pair import (
    SigningKeyPair,
)


def test_generates_key_pair():

    pair = SigningKeyPair.generate()

    assert pair.private_key is not None
    assert pair.public_key is not None


def test_keys_are_not_equal():

    pair = SigningKeyPair.generate()

    assert pair.private_key != pair.public_key
