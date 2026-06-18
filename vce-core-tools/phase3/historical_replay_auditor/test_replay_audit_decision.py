from phase3.historical_replay_auditor.replay_audit_decision import (
    ReplayAuditDecision,
)


def test_decision_contains_status():

    decision = ReplayAuditDecision(
        status="PASS"
    )

    assert decision.status == "PASS"


def test_decision_serializes():

    decision = ReplayAuditDecision(
        status="PASS"
    )

    assert decision.to_dict() == {
        "status": "PASS"
    }


def test_fail_decision_supported():

    decision = ReplayAuditDecision(
        status="FAIL"
    )

    assert decision.status == "FAIL"
