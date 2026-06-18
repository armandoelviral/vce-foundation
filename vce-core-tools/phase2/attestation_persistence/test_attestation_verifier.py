from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase2.attestation_persistence.attestation_verifier import (
    AttestationVerifier,
)


def test_verifier_accepts_matching_hash():

    record = AttestationRecord(
        attestation_id="att-001",
        subject="runtime-state",
        evidence_hash="hash-001",
    )

    assert (
        AttestationVerifier.verify(
            record,
            "hash-001",
        )
        is True
    )


def test_verifier_rejects_mismatch():

    record = AttestationRecord(
        attestation_id="att-001",
        subject="runtime-state",
        evidence_hash="hash-001",
    )

    assert (
        AttestationVerifier.verify(
            record,
            "hash-999",
        )
        is False
    )


def test_verifier_rejects_empty_hash():

    record = AttestationRecord(
        attestation_id="att-001",
        subject="runtime-state",
        evidence_hash="",
    )

    assert (
        AttestationVerifier.verify(
            record,
            ""
        )
        is False
    )
