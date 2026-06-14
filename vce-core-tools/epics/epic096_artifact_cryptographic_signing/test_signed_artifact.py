from epics.epic096_artifact_cryptographic_signing.signed_artifact import (
    SignedArtifact,
)


def test_signed_artifact_contains_signature():

    artifact = SignedArtifact(
        artifact_hash="artifact-hash-001",
        signature="signature-001",
        signer="signer-001",
    )

    assert artifact.artifact_hash == "artifact-hash-001"
    assert artifact.signature == "signature-001"
    assert artifact.signer == "signer-001"


def test_signed_artifact_serializes():

    artifact = SignedArtifact(
        artifact_hash="artifact-hash-001",
        signature="signature-001",
        signer="signer-001",
    )

    assert artifact.to_dict() == {
        "artifact_hash": "artifact-hash-001",
        "signature": "signature-001",
        "signer": "signer-001",
    }
