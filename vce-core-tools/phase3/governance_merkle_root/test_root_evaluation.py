from phase3.governance_merkle_root.governance_merkle_root_record import (
    GovernanceMerkleRootRecord,
)

from phase3.governance_merkle_root.root_evaluation import (
    RootEvaluation,
)


def test_valid_root_passes():

    root = GovernanceMerkleRootRecord(
        root_id="root-001",
        root_hash="root-hash-001",
        leaf_count=3,
    )

    assert (
        RootEvaluation.evaluate(
            root
        )
        is True
    )


def test_missing_root_id_fails():

    root = GovernanceMerkleRootRecord(
        root_id="",
        root_hash="root-hash-001",
        leaf_count=3,
    )

    assert (
        RootEvaluation.evaluate(
            root
        )
        is False
    )


def test_missing_root_hash_fails():

    root = GovernanceMerkleRootRecord(
        root_id="root-001",
        root_hash="",
        leaf_count=3,
    )

    assert (
        RootEvaluation.evaluate(
            root
        )
        is False
    )


def test_zero_leaf_count_fails():

    root = GovernanceMerkleRootRecord(
        root_id="root-001",
        root_hash="root-hash-001",
        leaf_count=0,
    )

    assert (
        RootEvaluation.evaluate(
            root
        )
        is False
    )
