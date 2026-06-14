from epics.epic096_artifact_cryptographic_signing.artifact_signer import (
    ArtifactSigner,
)

from epics.epic096_artifact_cryptographic_signing.signing_key_pair import (
    SigningKeyPair,
)


def test_signer_creates_signature():

    pair = SigningKeyPair.generate()

    signature = ArtifactSigner.sign(
        artifact_hash="artifact-hash-001",
        private_key=pair.private_key,
    )

    assert signature is not None
    assert len(signature) > 0


def test_signature_is_deterministic_for_same_key_and_hash():

    pair = SigningKeyPair.generate()

    signature_1 = ArtifactSigner.sign(
        artifact_hash="artifact-hash-001",
        private_key=pair.private_key,
    )

    signature_2 = ArtifactSigner.sign(
        artifact_hash="artifact-hash-001",
        private_key=pair.private_key,
    )

    assert signature_1 == signature_2
