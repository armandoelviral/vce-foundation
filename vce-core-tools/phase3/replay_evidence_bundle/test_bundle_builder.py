from phase3.replay_evidence_bundle.replay_evidence_record import (
    ReplayEvidenceRecord,
)

from phase3.replay_evidence_bundle.bundle_builder import (
    BundleBuilder,
)


def test_builder_creates_bundle_from_records():

    records = [
        ReplayEvidenceRecord(
            evidence_id="policy-001",
            evidence_type="policy",
        ),
        ReplayEvidenceRecord(
            evidence_id="witness-001",
            evidence_type="witness",
        ),
    ]

    bundle = BundleBuilder.build(
        records
    )

    assert bundle.count() == 2


def test_builder_preserves_record_order():

    records = [
        ReplayEvidenceRecord(
            evidence_id="policy-001",
            evidence_type="policy",
        ),
        ReplayEvidenceRecord(
            evidence_id="attestation-001",
            evidence_type="attestation",
        ),
    ]

    bundle = BundleBuilder.build(
        records
    )

    assert (
        bundle.records()[0].evidence_id
        == "policy-001"
    )

    assert (
        bundle.records()[1].evidence_id
        == "attestation-001"
    )


def test_builder_handles_empty_records():

    bundle = BundleBuilder.build(
        []
    )

    assert bundle.count() == 0
