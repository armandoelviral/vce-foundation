from epics.epic097_native_ed25519_signatures.ed25519_key_pair import (
    Ed25519KeyPair,
)

from epics.epic097_native_ed25519_signatures.native_ed25519_signer import (
    NativeEd25519Signer,
)

from epics.epic097_native_ed25519_signatures.native_trusted_signature_gate import (
    NativeTrustedSignatureGate,
)


def test_admits_valid_signature():

    pair = Ed25519KeyPair.generate()

    signature = NativeEd25519Signer.sign(
        artifact_hash="artifact-hash-001",
        private_key=pair.private_key,
    )

    assert NativeTrustedSignatureGate.admit(
        artifact_hash="artifact-hash-001",
        signature=signature,
        public_key=pair.public_key,
    )


def test_rejects_invalid_signature():

    pair = Ed25519KeyPair.generate()

    assert not NativeTrustedSignatureGate.admit(
        artifact_hash="artifact-hash-001",
        signature=b"tampered",
        public_key=pair.public_key,
    )
