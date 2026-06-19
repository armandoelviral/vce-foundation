from phase3.governance_merkle_root.governance_merkle_root_record import (
    GovernanceMerkleRootRecord,
)

from phase3.governance_merkle_root.root_report import (
    RootReport,
)


def test_report_contains_root_count():

    report = RootReport(
        {
            "root-001":
                GovernanceMerkleRootRecord(
                    root_id="root-001",
                    root_hash="root-hash-001",
                    leaf_count=3,
                )
        }
    )

    assert report.root_count() == 1


def test_report_lists_root_ids():

    report = RootReport(
        {
            "root-001":
                GovernanceMerkleRootRecord(
                    root_id="root-001",
                    root_hash="root-hash-001",
                    leaf_count=3,
                ),

            "root-002":
                GovernanceMerkleRootRecord(
                    root_id="root-002",
                    root_hash="root-hash-002",
                    leaf_count=5,
                ),
        }
    )

    assert report.root_ids() == [
        "root-001",
        "root-002",
    ]


def test_report_serializes():

    report = RootReport(
        {
            "root-001":
                GovernanceMerkleRootRecord(
                    root_id="root-001",
                    root_hash="root-hash-001",
                    leaf_count=3,
                )
        }
    )

    assert report.to_dict() == {
        "root_count": 1,
        "root_ids": [
            "root-001",
        ],
    }
