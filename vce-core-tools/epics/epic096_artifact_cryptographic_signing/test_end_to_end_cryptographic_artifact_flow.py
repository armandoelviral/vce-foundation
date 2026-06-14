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


def test_end_to_end_cryptographic_artifact_flow():

    pair = SigningKeyPair.generate()

    signature = ArtifactSigner.sign(
        artifact_hash="artifact-hash-001",
        private_key=pair.private_key,
    )

    artifact = SignedArtifact(
        artifact_hash="artifact-hash-001",
        signature=signature,
        signer="signer-001",
    )

    trusted = TrustedSignatureGate.admit(
        signed_artifact=artifact,
        private_key=pair.private_key,
    )

    assert trusted is True
