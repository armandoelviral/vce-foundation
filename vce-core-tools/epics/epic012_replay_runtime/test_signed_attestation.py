from epics.epic012_replay_runtime.signed_attestation import (
    SignedAttestation,
)


def test_signed_attestation_verifies_signed_payload():

    attestation = {
        "runtime": "VCE-RTE",
        "state_hash": "abc123",
        "verified": True,
    }

    signer = SignedAttestation()

    signed = signer.sign(
        attestation
    )

    assert (
        signer.verify(
            signed
        )
        is True
    )


def test_signed_attestation_contains_signature():

    attestation = {
        "runtime": "VCE-RTE",
        "state_hash": "abc123",
        "verified": True,
    }

    signer = SignedAttestation()

    signed = signer.sign(
        attestation
    )

    assert "signature" in signed
