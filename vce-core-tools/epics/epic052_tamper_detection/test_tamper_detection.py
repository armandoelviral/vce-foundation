from epics.epic047_snapshot_attestation.snapshot_attestation import (
    SnapshotAttestation,
)

from epics.epic050_cryptographic_signatures.signer import (
    Signer,
)

from epics.epic051_signed_snapshot_attestation.attestation_signer import (
    AttestationSigner,
)

from epics.epic051_signed_snapshot_attestation.signed_attestation import (
    SignedSnapshotAttestation,
)


def test_rejects_tampered_state_hash():

    attestation = SnapshotAttestation(
        sequence=42,
        state_hash="abc123",
    )

    signer = AttestationSigner(
        Signer(
            secret="test-secret"
        )
    )

    signed = signer.sign(
        attestation
    )

    tampered = SignedSnapshotAttestation(
        sequence=signed.sequence,
        state_hash="tampered",
        signature=signed.signature,
    )

    assert signer.verify(
        tampered
    ) is False

def test_rejects_tampered_sequence():

    attestation = SnapshotAttestation(
        sequence=42,
        state_hash="abc123",
    )

    signer = AttestationSigner(
        Signer(
            secret="test-secret"
        )
    )

    signed = signer.sign(
        attestation
    )

    tampered = SignedSnapshotAttestation(
        sequence=999,
        state_hash=signed.state_hash,
        signature=signed.signature,
    )

    assert signer.verify(
        tampered
    ) is False
