from epics.epic097_native_ed25519_signatures.ed25519_key_pair import (
    Ed25519KeyPair,
)

from epics.epic097_native_ed25519_signatures.native_ed25519_signer import (
    NativeEd25519Signer,
)


def test_signs_artifact_hash():

    pair = Ed25519KeyPair.generate()

    signature = NativeEd25519Signer.sign(
        artifact_hash="artifact-hash-001",
        private_key=pair.private_key,
    )

    assert isinstance(signature, bytes)
    assert len(signature) > 0


def test_same_message_produces_same_signature():

    pair = Ed25519KeyPair.generate()

    signature_1 = NativeEd25519Signer.sign(
        artifact_hash="artifact-hash-001",
        private_key=pair.private_key,
    )

    signature_2 = NativeEd25519Signer.sign(
        artifact_hash="artifact-hash-001",
        private_key=pair.private_key,
    )

    assert signature_1 == signature_2
