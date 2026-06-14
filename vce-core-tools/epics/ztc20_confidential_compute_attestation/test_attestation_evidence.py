from epics.ztc20_confidential_compute_attestation.attestation_evidence import (
    AttestationEvidence,
)


def test_contains_witness_id():

    evidence = AttestationEvidence(
        witness_id="witness-001",
        provider="aws",
        evidence_hash="hash-001",
    )

    assert evidence.witness_id == "witness-001"


def test_contains_provider():

    evidence = AttestationEvidence(
        witness_id="witness-001",
        provider="aws",
        evidence_hash="hash-001",
    )

    assert evidence.provider == "aws"


def test_contains_evidence_hash():

    evidence = AttestationEvidence(
        witness_id="witness-001",
        provider="aws",
        evidence_hash="hash-001",
    )

    assert evidence.evidence_hash == "hash-001"


def test_serializes():

    evidence = AttestationEvidence(
        witness_id="witness-001",
        provider="aws",
        evidence_hash="hash-001",
    )

    assert evidence.to_dict() == {
        "witness_id": "witness-001",
        "provider": "aws",
        "evidence_hash": "hash-001",
    }
