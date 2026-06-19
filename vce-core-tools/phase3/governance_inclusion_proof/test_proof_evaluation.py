from phase3.governance_inclusion_proof.inclusion_proof_record import (
    InclusionProofRecord,
)

from phase3.governance_inclusion_proof.proof_evaluation import (
    ProofEvaluation,
)


def test_valid_proof_passes():

    proof = InclusionProofRecord(
        leaf_id="leaf-001",
        root_id="root-001",
        proof_hash="proof-hash-001",
    )

    assert (
        ProofEvaluation.evaluate(
            proof
        )
        is True
    )


def test_missing_leaf_id_fails():

    proof = InclusionProofRecord(
        leaf_id="",
        root_id="root-001",
        proof_hash="proof-hash-001",
    )

    assert (
        ProofEvaluation.evaluate(
            proof
        )
        is False
    )


def test_missing_root_id_fails():

    proof = InclusionProofRecord(
        leaf_id="leaf-001",
        root_id="",
        proof_hash="proof-hash-001",
    )

    assert (
        ProofEvaluation.evaluate(
            proof
        )
        is False
    )


def test_missing_proof_hash_fails():

    proof = InclusionProofRecord(
        leaf_id="leaf-001",
        root_id="root-001",
        proof_hash="",
    )

    assert (
        ProofEvaluation.evaluate(
            proof
        )
        is False
    )
