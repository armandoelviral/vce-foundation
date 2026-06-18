from phase3.replay_evidence_bundle.replay_evidence_record import (
    ReplayEvidenceRecord,
)

from phase3.replay_evidence_bundle.bundle_builder import (
    BundleBuilder,
)

from phase3.replay_evidence_bundle.bundle_query import (
    BundleQuery,
)


def test_query_returns_record_by_id():

    bundle = BundleBuilder.build(
        [
            ReplayEvidenceRecord(
                evidence_id="policy-001",
                evidence_type="policy",
            )
        ]
    )

    query = BundleQuery(bundle)

    result = query.by_id(
        "policy-001"
    )

    assert result.evidence_id == "policy-001"


def test_query_returns_none_for_missing_id():

    bundle = BundleBuilder.build([])

    query = BundleQuery(bundle)

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_correct_type():

    bundle = BundleBuilder.build(
        [
            ReplayEvidenceRecord(
                evidence_id="attestation-001",
                evidence_type="attestation",
            )
        ]
    )

    query = BundleQuery(bundle)

    result = query.by_id(
        "attestation-001"
    )

    assert (
        result.evidence_type
        == "attestation"
    )
