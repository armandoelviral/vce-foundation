from phase3.replay_evidence_bundle.replay_evidence_record import (
    ReplayEvidenceRecord,
)

from phase3.replay_evidence_bundle.bundle_builder import (
    BundleBuilder,
)

from phase3.replay_evidence_bundle.bundle_attestation import (
    BundleAttestation,
)


def test_attestation_subject():

    bundle = BundleBuilder.build(
        [
            ReplayEvidenceRecord(
                evidence_id="policy-001",
                evidence_type="policy",
            )
        ]
    )

    attestation = BundleAttestation.attest(
        attestation_id="att-001",
        bundle=bundle,
    )

    assert attestation.subject == "replay_bundle"


def test_attestation_preserves_id():

    bundle = BundleBuilder.build(
        [
            ReplayEvidenceRecord(
                evidence_id="policy-001",
                evidence_type="policy",
            )
        ]
    )

    attestation = BundleAttestation.attest(
        attestation_id="att-001",
        bundle=bundle,
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )


def test_attestation_uses_bundle_size_as_evidence():

    bundle = BundleBuilder.build(
        [
            ReplayEvidenceRecord(
                evidence_id="policy-001",
                evidence_type="policy",
            )
        ]
    )

    attestation = BundleAttestation.attest(
        attestation_id="att-001",
        bundle=bundle,
    )

    assert (
        attestation.evidence_hash
        == "1"
    )
