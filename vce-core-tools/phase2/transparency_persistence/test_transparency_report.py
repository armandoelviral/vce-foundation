from phase2.transparency_persistence.merkle_root_record import (
    MerkleRootRecord,
)

from phase2.transparency_persistence.transparency_report import (
    TransparencyReport,
)


def test_report_contains_total_roots():

    roots = [
        MerkleRootRecord(
            root_hash="root-001",
            entry_count=5,
        ),
        MerkleRootRecord(
            root_hash="root-002",
            entry_count=10,
        ),
    ]

    report = TransparencyReport(
        roots
    )

    assert report.total_roots() == 2


def test_report_lists_root_hashes():

    roots = [
        MerkleRootRecord(
            root_hash="root-001",
            entry_count=5,
        ),
        MerkleRootRecord(
            root_hash="root-002",
            entry_count=10,
        ),
    ]

    report = TransparencyReport(
        roots
    )

    assert report.root_hashes() == [
        "root-001",
        "root-002",
    ]


def test_report_serializes():

    roots = [
        MerkleRootRecord(
            root_hash="root-001",
            entry_count=5,
        )
    ]

    report = TransparencyReport(
        roots
    )

    assert report.to_dict() == {
        "total_roots": 1,
        "root_hashes": [
            "root-001",
        ],
    }
