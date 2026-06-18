from phase3.replay_evidence_bundle.replay_evidence_record import (
    ReplayEvidenceRecord,
)

from phase3.replay_evidence_bundle.bundle_builder import (
    BundleBuilder,
)

from phase3.replay_evidence_bundle.bundle_verifier import (
    BundleVerifier,
)


def test_verifier_accepts_non_empty_bundle():

    bundle = BundleBuilder.build(
        [
            ReplayEvidenceRecord(
                evidence_id="policy-001",
                evidence_type="policy",
            )
        ]
    )

    assert BundleVerifier.verify(bundle) is True


def test_verifier_rejects_empty_bundle():

    bundle = BundleBuilder.build([])

    assert BundleVerifier.verify(bundle) is False


def test_verifier_rejects_missing_evidence_id():

    bundle = BundleBuilder.build(
        [
            ReplayEvidenceRecord(
                evidence_id="",
                evidence_type="policy",
            )
        ]
    )

    assert BundleVerifier.verify(bundle) is False
