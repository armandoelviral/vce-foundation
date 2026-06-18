from phase3.historical_replay_auditor.historical_replay_record import (
    HistoricalReplayRecord,
)

from phase3.historical_replay_auditor.replay_evidence_resolver import (
    ReplayEvidenceResolver,
)

from phase3.historical_replay_auditor.replay_auditor import (
    ReplayAuditor,
)

from phase3.historical_replay_auditor.replay_audit_decision import (
    ReplayAuditDecision,
)

from phase3.historical_replay_auditor.replay_certification import (
    ReplayCertification,
)

from phase3.historical_replay_auditor.historical_replay_report import (
    HistoricalReplayReport,
)

from phase3.replay_evidence_bundle.replay_evidence_bundle import (
    ReplayEvidenceBundle,
)

from phase3.replay_evidence_bundle.replay_evidence_record import (
    ReplayEvidenceRecord,
)


def test_end_to_end_historical_replay_auditor():

    bundle = ReplayEvidenceBundle()

    bundle.add(
        ReplayEvidenceRecord(
            evidence_id="policy-001",
            evidence_type="policy",
        )
    )

    replay = HistoricalReplayRecord(
        replay_id="replay-001",
        bundle_id="bundle-001",
    )

    resolved_bundle = (
        ReplayEvidenceResolver.resolve(
            replay,
            {"bundle-001": bundle},
        )
    )

    assert resolved_bundle is not None

    audit_result = (
        ReplayAuditor.audit(
            resolved_bundle
        )
    )

    assert audit_result is True

    decision = ReplayAuditDecision(
        status="PASS"
    )

    certification = (
        ReplayCertification.certify(
            decision
        )
    )

    assert certification.certified is True

    report = HistoricalReplayReport(
        certification
    )

    assert report.status() == "PASS"

    assert report.certified() is True
