from phase3.replay_evidence_bundle.replay_evidence_record import (
    ReplayEvidenceRecord,
)

from phase3.replay_evidence_bundle.bundle_builder import (
    BundleBuilder,
)

from phase3.replay_evidence_bundle.bundle_report import (
    BundleReport,
)


def test_report_contains_record_count():

    bundle = BundleBuilder.build(
        [
            ReplayEvidenceRecord(
                evidence_id="policy-001",
                evidence_type="policy",
            ),
            ReplayEvidenceRecord(
                evidence_id="witness-001",
                evidence_type="witness",
            ),
        ]
    )

    report = BundleReport(bundle)

    assert report.record_count() == 2


def test_report_lists_evidence_ids():

    bundle = BundleBuilder.build(
        [
            ReplayEvidenceRecord(
                evidence_id="policy-001",
                evidence_type="policy",
            ),
            ReplayEvidenceRecord(
                evidence_id="witness-001",
                evidence_type="witness",
            ),
        ]
    )

    report = BundleReport(bundle)

    assert report.evidence_ids() == [
        "policy-001",
        "witness-001",
    ]


def test_report_serializes():

    bundle = BundleBuilder.build(
        [
            ReplayEvidenceRecord(
                evidence_id="policy-001",
                evidence_type="policy",
            )
        ]
    )

    report = BundleReport(bundle)

    assert report.to_dict() == {
        "record_count": 1,
        "evidence_ids": [
            "policy-001",
        ],
    }
