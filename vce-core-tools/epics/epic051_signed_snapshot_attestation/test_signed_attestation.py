from epics.epic047_snapshot_attestation.snapshot_attestation import (
    SnapshotAttestation,
)
from epics.epic050_cryptographic_signatures.signer import Signer
from epics.epic051_signed_snapshot_attestation.signed_attestation import (
    SignedSnapshotAttestation,
)
from epics.epic051_signed_snapshot_attestation.attestation_signer import (
    AttestationSigner,
)


def test_signs_snapshot_attestation():

    attestation = SnapshotAttestation(
        sequence=42,
        state_hash="abc123",
    )

    signer = AttestationSigner(
        Signer(secret="test-secret")
    )

    signed = signer.sign(attestation)

    assert isinstance(signed, SignedSnapshotAttestation)
    assert signed.sequence == 42
    assert signed.state_hash == "abc123"
    assert isinstance(signed.signature, str)
    assert len(signed.signature) == 64


def test_verifies_signed_snapshot_attestation():

    attestation = SnapshotAttestation(
        sequence=42,
        state_hash="abc123",
    )

    signer = AttestationSigner(
        Signer(secret="test-secret")
    )

    signed = signer.sign(attestation)

    assert signer.verify(signed) is True
