from phase3.governance_inclusion_proof.inclusion_proof_record import (
    InclusionProofRecord,
)

from phase3.governance_inclusion_proof.proof_registry import (
    ProofRegistry,
)

from phase3.governance_inclusion_proof.proof_query import (
    ProofQuery,
)


def test_query_returns_proof():

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

    query = ProofQuery(
        registry
    )

    result = query.by_id(
        "proof-001"
    )

    assert result == proof


def test_query_returns_none_for_missing():

    registry = ProofRegistry()

    query = ProofQuery(
        registry
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_root_id():

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

    query = ProofQuery(
        registry
    )

    result = query.by_id(
        "proof-001"
    )

    assert (
        result.root_id
        == "root-001"
    )
