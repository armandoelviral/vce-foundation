from phase3.replay_evidence_bundle.replay_evidence_record import (
    ReplayEvidenceRecord,
)

from phase3.replay_evidence_bundle.bundle_builder import (
    BundleBuilder,
)

from phase3.replay_evidence_bundle.bundle_verifier import (
    BundleVerifier,
)

from phase3.replay_evidence_bundle.bundle_query import (
    BundleQuery,
)

from phase3.replay_evidence_bundle.bundle_report import (
    BundleReport,
)

from phase3.replay_evidence_bundle.bundle_attestation import (
    BundleAttestation,
)


def test_end_to_end_replay_bundle():

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

    assert (
        BundleVerifier.verify(
            bundle
        )
        is True
    )

    query = BundleQuery(
        bundle
    )

    record = query.by_id(
        "policy-001"
    )

    assert record is not None

    report = BundleReport(
        bundle
    )

    assert report.record_count() == 2

    attestation = (
        BundleAttestation.attest(
            attestation_id="att-001",
            bundle=bundle,
        )
    )

    assert (
        attestation.subject
        == "replay_bundle"
    )
