from phase3.historical_replay_auditor.replay_auditor import (
    ReplayAuditor,
)

from phase3.replay_evidence_bundle.replay_evidence_bundle import (
    ReplayEvidenceBundle,
)

from phase3.replay_evidence_bundle.replay_evidence_record import (
    ReplayEvidenceRecord,
)


def test_auditor_accepts_bundle_with_evidence():

    bundle = ReplayEvidenceBundle()

    bundle.add(
        ReplayEvidenceRecord(
            evidence_id="policy-001",
            evidence_type="policy",
        )
    )

    assert (
        ReplayAuditor.audit(
            bundle
        )
        is True
    )


def test_auditor_rejects_empty_bundle():

    bundle = ReplayEvidenceBundle()

    assert (
        ReplayAuditor.audit(
            bundle
        )
        is False
    )


def test_auditor_rejects_none_bundle():

    assert (
        ReplayAuditor.audit(
            None
        )
        is False
    )
