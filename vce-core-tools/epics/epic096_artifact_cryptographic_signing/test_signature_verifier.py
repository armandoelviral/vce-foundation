from epics.epic096_artifact_cryptographic_signing.artifact_signer import (
    ArtifactSigner,
)

from epics.epic096_artifact_cryptographic_signing.signature_verifier import (
    SignatureVerifier,
)

from epics.epic096_artifact_cryptographic_signing.signing_key_pair import (
    SigningKeyPair,
)


def test_accepts_valid_signature():

    pair = SigningKeyPair.generate()

    signature = ArtifactSigner.sign(
        artifact_hash="artifact-hash-001",
        private_key=pair.private_key,
    )

    assert SignatureVerifier.verify(
        artifact_hash="artifact-hash-001",
        signature=signature,
        private_key=pair.private_key,
    )


def test_rejects_tampered_signature():

    pair = SigningKeyPair.generate()

    assert not SignatureVerifier.verify(
        artifact_hash="artifact-hash-001",
        signature="tampered-signature",
        private_key=pair.private_key,
    )
