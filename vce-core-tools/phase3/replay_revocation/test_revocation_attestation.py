from phase3.replay_revocation.replay_revocation_record import (
    ReplayRevocationRecord,
)

from phase3.replay_revocation.revocation_attestation import (
    RevocationAttestation,
)


def test_attestation_subject():

    revocation = ReplayRevocationRecord(
        revocation_id="rev-001",
        certificate_id="cert-001",
        reason="key_compromise",
    )

    attestation = (
        RevocationAttestation.attest(
            attestation_id="att-001",
            revocation=revocation,
        )
    )

    assert (
        attestation.subject
        == "replay_revocation"
    )


def test_attestation_uses_revocation_id():

    revocation = ReplayRevocationRecord(
        revocation_id="rev-001",
        certificate_id="cert-001",
        reason="key_compromise",
    )

    attestation = (
        RevocationAttestation.attest(
            attestation_id="att-001",
            revocation=revocation,
        )
    )

    assert (
        attestation.evidence_hash
        == "rev-001"
    )


def test_attestation_preserves_id():

    revocation = ReplayRevocationRecord(
        revocation_id="rev-001",
        certificate_id="cert-001",
        reason="key_compromise",
    )

    attestation = (
        RevocationAttestation.attest(
            attestation_id="att-001",
            revocation=revocation,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
