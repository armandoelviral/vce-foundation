from epics.epic096_artifact_cryptographic_signing.artifact_signer import (
    ArtifactSigner,
)

from epics.epic096_artifact_cryptographic_signing.signing_key_pair import (
    SigningKeyPair,
)

from epics.epic096_artifact_cryptographic_signing.signed_artifact import (
    SignedArtifact,
)

from epics.epic096_artifact_cryptographic_signing.trusted_signature_gate import (
    TrustedSignatureGate,
)


def test_admits_valid_signed_artifact():

    pair = SigningKeyPair.generate()

    signature = ArtifactSigner.sign(
        artifact_hash="artifact-hash-001",
        private_key=pair.private_key,
    )

    signed_artifact = SignedArtifact(
        artifact_hash="artifact-hash-001",
        signature=signature,
        signer="signer-001",
    )

    assert TrustedSignatureGate.admit(
        signed_artifact=signed_artifact,
        private_key=pair.private_key,
    )


def test_rejects_tampered_signed_artifact():

    pair = SigningKeyPair.generate()

    signed_artifact = SignedArtifact(
        artifact_hash="artifact-hash-001",
        signature="tampered-signature",
        signer="signer-001",
    )

    assert not TrustedSignatureGate.admit(
        signed_artifact=signed_artifact,
        private_key=pair.private_key,
    )
