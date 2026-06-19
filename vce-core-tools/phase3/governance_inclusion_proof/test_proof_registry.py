from phase3.governance_inclusion_proof.inclusion_proof_record import (
    InclusionProofRecord,
)

from phase3.governance_inclusion_proof.proof_registry import (
    ProofRegistry,
)


def test_registry_starts_empty():

    registry = ProofRegistry()

    assert registry.count() == 0


def test_registry_accepts_proof():

    registry = ProofRegistry()

    proof = InclusionProofRecord(
        leaf_id="leaf-001",
        root_id="root-001",
        proof_hash="proof-hash-001",
    )

    registry.add(
        proof_id="proof-001",
        proof=proof,
    )

    assert registry.count() == 1


def test_registry_returns_proof():

    registry = ProofRegistry()

    proof = InclusionProofRecord(
        leaf_id="leaf-001",
        root_id="root-001",
        proof_hash="proof-hash-001",
    )

    registry.add(
        proof_id="proof-001",
        proof=proof,
    )

    recovered = registry.get(
        "proof-001"
    )

    assert recovered == proof


def test_missing_proof_returns_none():

    registry = ProofRegistry()

    assert registry.get(
        "missing"
    ) is None


def test_registry_lists_proof_ids():

    registry = ProofRegistry()

    registry.add(
        proof_id="proof-001",
        proof=InclusionProofRecord(
            leaf_id="leaf-001",
            root_id="root-001",
            proof_hash="proof-hash-001",
        ),
    )

    registry.add(
        proof_id="proof-002",
        proof=InclusionProofRecord(
            leaf_id="leaf-002",
            root_id="root-001",
            proof_hash="proof-hash-002",
        ),
    )

    assert registry.proof_ids() == [
        "proof-001",
        "proof-002",
    ]
