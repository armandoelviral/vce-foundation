from phase3.governance_escalation.escalation_record import (
    EscalationRecord,
)

from phase3.governance_escalation.suspension_evaluation import (
    SuspensionEvaluation,
)


def test_high_severity_requires_suspension():

    record = EscalationRecord(
        escalation_id="esc-001",
        reason="quorum_failure",
        severity="HIGH",
    )

    result = SuspensionEvaluation.evaluate(
        record
    )

    assert result is True


def test_medium_severity_does_not_suspend():

    record = EscalationRecord(
        escalation_id="esc-002",
        reason="manual_review",
        severity="MEDIUM",
    )

    result = SuspensionEvaluation.evaluate(
        record
    )

    assert result is False


def test_low_severity_does_not_suspend():

    record = EscalationRecord(
        escalation_id="esc-003",
        reason="notification",
        severity="LOW",
    )

    result = SuspensionEvaluation.evaluate(
        record
    )

    assert result is False
