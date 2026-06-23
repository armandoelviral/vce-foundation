from phase4.reputation_constitution_layer.reputation_evidence import (
    ReputationEvidence,
)


def test_contains_claim_id():
    evidence = ReputationEvidence(
        claim_id="claim-001",
        evidence_hash="hash-001",
    )

    assert evidence.claim_id == "claim-001"


def test_contains_evidence_hash():
    evidence = ReputationEvidence(
        claim_id="claim-001",
        evidence_hash="hash-001",
    )

    assert evidence.evidence_hash == "hash-001"


def test_serializes():
    evidence = ReputationEvidence(
        claim_id="claim-001",
        evidence_hash="hash-001",
    )

    assert evidence.to_dict() == {
        "claim_id": "claim-001",
        "evidence_hash": "hash-001",
    }
