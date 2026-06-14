from epics.epic097_native_ed25519_signatures.ed25519_key_pair import (
    Ed25519KeyPair,
)

from epics.epic097_native_ed25519_signatures.native_ed25519_signer import (
    NativeEd25519Signer,
)

from epics.epic097_native_ed25519_signatures.native_ed25519_verifier import (
    NativeEd25519Verifier,
)


def test_verifies_valid_signature():

    pair = Ed25519KeyPair.generate()

    signature = NativeEd25519Signer.sign(
        artifact_hash="artifact-hash-001",
        private_key=pair.private_key,
    )

    assert NativeEd25519Verifier.verify(
        artifact_hash="artifact-hash-001",
        signature=signature,
        public_key=pair.public_key,
    )


def test_rejects_invalid_signature():

    pair = Ed25519KeyPair.generate()

    assert not NativeEd25519Verifier.verify(
        artifact_hash="artifact-hash-001",
        signature=b"invalid-signature",
        public_key=pair.public_key,
    )
