from phase3.historical_replay_auditor.replay_audit_decision import (
    ReplayAuditDecision,
)

from phase3.historical_replay_auditor.replay_certification import (
    ReplayCertification,
)


def test_certification_contains_status():

    decision = ReplayAuditDecision(
        status="PASS"
    )

    certification = ReplayCertification.certify(
        decision
    )

    assert certification.status == "PASS"


def test_pass_decision_certifies():

    decision = ReplayAuditDecision(
        status="PASS"
    )

    certification = ReplayCertification.certify(
        decision
    )

    assert certification.certified is True


def test_fail_decision_not_certified():

    decision = ReplayAuditDecision(
        status="FAIL"
    )

    certification = ReplayCertification.certify(
        decision
    )

    assert certification.certified is False
