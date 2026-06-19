from phase3.governance_merkle_history.governance_merkle_leaf import (
    GovernanceMerkleLeaf,
)

from phase3.governance_merkle_history.merkle_history_evaluation import (
    MerkleHistoryEvaluation,
)


def test_valid_leaf_passes():

    leaf = GovernanceMerkleLeaf(
        leaf_id="leaf-001",
        snapshot_id="snap-001",
        hash_value="hash-001",
    )

    assert (
        MerkleHistoryEvaluation.evaluate(
            leaf
        )
        is True
    )


def test_missing_leaf_id_fails():

    leaf = GovernanceMerkleLeaf(
        leaf_id="",
        snapshot_id="snap-001",
        hash_value="hash-001",
    )

    assert (
        MerkleHistoryEvaluation.evaluate(
            leaf
        )
        is False
    )


def test_missing_snapshot_id_fails():

    leaf = GovernanceMerkleLeaf(
        leaf_id="leaf-001",
        snapshot_id="",
        hash_value="hash-001",
    )

    assert (
        MerkleHistoryEvaluation.evaluate(
            leaf
        )
        is False
    )


def test_missing_hash_value_fails():

    leaf = GovernanceMerkleLeaf(
        leaf_id="leaf-001",
        snapshot_id="snap-001",
        hash_value="",
    )

    assert (
        MerkleHistoryEvaluation.evaluate(
            leaf
        )
        is False
    )
