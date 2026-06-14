from epics.ztc20_confidential_compute_attestation.attestation_evidence import (
    AttestationEvidence,
)

from epics.ztc20_confidential_compute_attestation.attestation_verifier import (
    AttestationVerifier,
)


def test_accepts_valid_attestation():

    evidence = AttestationEvidence(
        witness_id="witness-001",
        provider="aws",
        evidence_hash="hash-001",
    )

    assert AttestationVerifier.verify(evidence)


def test_rejects_missing_witness_id():

    evidence = AttestationEvidence(
        witness_id="",
        provider="aws",
        evidence_hash="hash-001",
    )

    assert not AttestationVerifier.verify(evidence)


def test_rejects_unsupported_provider():

    evidence = AttestationEvidence(
        witness_id="witness-001",
        provider="unknown",
        evidence_hash="hash-001",
    )

    assert not AttestationVerifier.verify(evidence)


def test_rejects_missing_evidence_hash():

    evidence = AttestationEvidence(
        witness_id="witness-001",
        provider="aws",
        evidence_hash="",
    )

    assert not AttestationVerifier.verify(evidence)
