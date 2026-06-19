from phase3.governance_merkle_history.governance_merkle_leaf import (
    GovernanceMerkleLeaf,
)

from phase3.governance_merkle_history.merkle_history_report import (
    MerkleHistoryReport,
)


def test_report_contains_leaf_count():

    report = MerkleHistoryReport(
        {
            "leaf-001":
                GovernanceMerkleLeaf(
                    leaf_id="leaf-001",
                    snapshot_id="snap-001",
                    hash_value="hash-001",
                )
        }
    )

    assert report.leaf_count() == 1


def test_report_lists_leaf_ids():

    report = MerkleHistoryReport(
        {
            "leaf-001":
                GovernanceMerkleLeaf(
                    leaf_id="leaf-001",
                    snapshot_id="snap-001",
                    hash_value="hash-001",
                ),

            "leaf-002":
                GovernanceMerkleLeaf(
                    leaf_id="leaf-002",
                    snapshot_id="snap-002",
                    hash_value="hash-002",
                ),
        }
    )

    assert report.leaf_ids() == [
        "leaf-001",
        "leaf-002",
    ]


def test_report_serializes():

    report = MerkleHistoryReport(
        {
            "leaf-001":
                GovernanceMerkleLeaf(
                    leaf_id="leaf-001",
                    snapshot_id="snap-001",
                    hash_value="hash-001",
                )
        }
    )

    assert report.to_dict() == {
        "leaf_count": 1,
        "leaf_ids": [
            "leaf-001",
        ],
    }
