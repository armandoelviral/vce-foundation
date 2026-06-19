from phase3.governance_inclusion_proof.inclusion_proof_record import (
    InclusionProofRecord,
)


def test_contains_leaf_id():

    proof = InclusionProofRecord(
        leaf_id="leaf-001",
        root_id="root-001",
        proof_hash="proof-hash-001",
    )

    assert proof.leaf_id == "leaf-001"


def test_contains_root_id():

    proof = InclusionProofRecord(
        leaf_id="leaf-001",
        root_id="root-001",
        proof_hash="proof-hash-001",
    )

    assert proof.root_id == "root-001"


def test_contains_proof_hash():

    proof = InclusionProofRecord(
        leaf_id="leaf-001",
        root_id="root-001",
        proof_hash="proof-hash-001",
    )

    assert proof.proof_hash == "proof-hash-001"


def test_serializes():

    proof = InclusionProofRecord(
        leaf_id="leaf-001",
        root_id="root-001",
        proof_hash="proof-hash-001",
    )

    assert proof.to_dict() == {
        "leaf_id": "leaf-001",
        "root_id": "root-001",
        "proof_hash": "proof-hash-001",
    }
